from flask import render_template, url_for, flash, redirect, request, session, g
from PRA.forms import RegistrationForm, UpdateForm, LoginForm, ContactForm, ModelForm, NerForm, ComplaintForm
from PRA import app, mongo, bcrypt
from PRA.utils import sentiment_score, process_tweet, tweet_wrapper, extract_ne
from PRA.twitter_fetch import hashtag_tweets, followers
from PRA.chart_data import total_tweets, positive_count, negative_count, wordcloud_data, wordcloud_data_neg, tweets_location
from flask_paginate import Pagination, get_page_parameter

# followers count commented out purposely to save twitter api calls, enable it while demonstrating project
# followers=followers(g.twitter) add this on /home and /analysis route

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/registration',methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        keywords = form.keywords.data.split()
        user_profile = {
            "FullName": form.fullname.data, "Organization" : form.organization.data,
            "Email": form.email.data,"Password": hashed_password, "OrganizationType": form.organization_type.data,
            "TwitterAccount": form.twitter_id.data, "FacebookLink": form.facebook_link.data, 
            "Keywords":keywords }
        mongo.db.user.insert_one(user_profile)   
        flash('Registration Successful, Login to continue.','success')
        return redirect('login')
    return render_template('auth-register.html',form=form)

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    session.pop('user',None )
    session.pop('username',None )
    session.pop('orgname',None )
    session.pop('twiiter',None)

    if request.method == 'POST':
        user_data = mongo.db.user.find_one({"Email": form.email.data},{"_id":0 ,"Email":1, "Password":1,
                                                        "TwitterAccount":1,"FullName":1, "Organization":1})
        if user_data:
            if bcrypt.check_password_hash(user_data["Password"], form.password.data):
                session['user'] = user_data['Email']
                session['username'] = user_data['FullName']
                session['orgname'] = user_data['Organization']
                session['twitter'] = user_data['TwitterAccount']
                return redirect(url_for('home'))
            else:  
                flash('Incorrect password.')  
        else:
            flash('Email does not exist.')
    return render_template('auth-login.html',form=form)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
    if 'username' in session:
        g.username = session['username']
    if 'orgname' in session:
        g.orgname = session['orgname']
    if 'twitter' in session:
        g.twitter = session['twitter']            
        
@app.route('/logout')
def logout():
    session.pop('user',None)
    session.pop('username', None)
    session.pop('orgname', None)
    session.pop('twitter', None)
    return redirect('index')

@app.route('/home',methods=['GET','POST'])
def home():
    if g.user:
        return render_template('home.html',positive_count=positive_count(),negative_count=negative_count(),
        total_tweets=total_tweets(),words=wordcloud_data(),neg_words=wordcloud_data_neg(),locations=tweets_location())
    return redirect('login')    

@app.route('/update',methods=['GET','POST'])
def update():
    form = UpdateForm()
    if g.user:
        if request.method == 'GET':
            user_data = mongo.db.user.find_one({"Email": g.user},{"_id":0 ,"Email":1,"TwitterAccount":1,"FacebookLink":1,
                                                                        "Keywords":1,"FullName":1, "Organization":1})
            keywords = ' '.join([str(i) for i in user_data['Keywords']])                                                         
            form.fullname.data = user_data["FullName"]
            form.organization.data = user_data["Organization"]
            form.email.data = user_data["Email"]
            form.twitter_id.data = user_data["TwitterAccount"]
            form.facebook_link.data = user_data["FacebookLink"]   
            form.keywords.data = keywords                                                      
        
        if request.method == 'POST':
            keywords_list = form.keywords.data.split() 
            mongo.db.user.update({"Email":g.user},{ '$set' : {'FullName' :form.fullname.data, 'Organization':form.organization.data, 
                                        'Email':form.email.data,'TwitterAccount':form.twitter_id.data, 
                                        'FacebookLink':form.facebook_link.data, 'Keywords':keywords_list}})                            
            flash('Profile Updated.')
            return redirect('update')
        return render_template('update-profile.html',form=form)
    return redirect('login')    
    

@app.route('/contact',methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        mongo.db.feedback.insert_one({"Name": form.name.data,"Email": form.email.data, "Message": form.message.data })
        flash("We've received your message.")
    return render_template('contact.html', form=form)

@app.route('/tweets',methods=['GET','POST'])
def tweets():
    if g.user:
        search = False
        q = request.args.get('q')
        if q:
            search = True
        page = request.args.get(get_page_parameter(), type=int, default=1)
        tweets = mongo.db.tweets.find({"User": g.user},{"_id":0 ,"Tweet.Text":1,"Tweet.Polarity":1,"Tweet.confidence":1})
        pagination = Pagination(page=page,css_framework='bootstrap', total=tweets.count(), 
        per_page=20,bs_version=4,search=search, record_name='tweets')
        return render_template('tweets.html',tweets=tweets,pagination=pagination)
    return redirect('login')

@app.route('/sentiment', methods=['GET','POST'])
def sentiment():
    if g.user:
        form = ModelForm()
        score = 0
        polarity = ''
        if request.method == 'POST':
            text = tweet_wrapper(form.text.data)
            result= sentiment_score(text)
            score = result[2]
            polarity = result[1]    
        return render_template('sentiment.html',form=form,polarity=polarity,score=score)
    return redirect('login')

@app.route('/analysis',methods=['GET','POST'])
def analysis():
    if g.user:
        keywords = mongo.db.user.find_one({"Email":g.user },{"_id":0 ,"Keywords":1})
        keywords_list = list(keywords.values())
        try:
            tweets = hashtag_tweets(keywords_list[0])
            locations = tweets[1]
            processed_tweet =[]
            analyzed_tweet = []
            for tweet in tweets[0]:
                processed_tweet.append(process_tweet(tweet))
            for i in processed_tweet:
                analyzed_tweet.append(sentiment_score(i)) 
            for tweet_data,loc in zip(analyzed_tweet,locations):
                mongo.db.tweets.insert_one({"User":g.user,"Tweet": {
                    "Text":tweet_data[0],"Polarity":tweet_data[1],"confidence":tweet_data[2],"Location":loc
                }})    
            flash("we've collected & analyzed recent 200 tweets. scroll down for more info.")
        except:
            flash("You've reached twitter API calls limit. Please try again after sometimes.")
        return render_template('home.html',positive_count=positive_count(),negative_count=negative_count(),
        total_tweets=total_tweets(),locations=tweets_location(),words=wordcloud_data(),neg_words=wordcloud_data_neg())
    return redirect('login')    

@app.route('/ner',methods=['GET','POST'])
def ner():
    if g.user:
        form = NerForm()
        result = ''
        if request.method == 'POST':
            result = extract_ne(form.text.data)
        return render_template('ner.html',form=form,result=result)
    return redirect('login')

@app.route('/complaint',methods=['GET','POST'])
def complaint():
    if g.user:
        form = ComplaintForm()
        result = ''
        if request.method == 'POST':
            result = extract_ne(form.text.data)
        return render_template('complaint.html',form=form,result=result)
    return redirect('login')