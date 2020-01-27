from flask import render_template, url_for, flash, redirect, request, abort, jsonify, json, session, g
from PRA.forms import RegistrationForm, UpdateForm, LoginForm, ContactForm, ModelForm
from PRA import app, mongo, bcrypt

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory('static/landing-assets/img/favicon.ico')

@app.route('/index')
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

    if request.method == 'POST':
        user_data = mongo.db.user.find_one({"Email": form.email.data},{"_id":0 ,"Email":1, "Password":1,
                                                                             "FullName":1, "Organization":1})
        if user_data:
            if bcrypt.check_password_hash(user_data["Password"], form.password.data):
                session['user'] = user_data['Email']
                session['username'] = user_data['FullName']
                session['orgname'] = user_data['Organization']
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
        
@app.route('/logout')
def logout():
    session.pop('user',None)
    session.pop('username', None)
    session.pop('orgname', None)
    return redirect('index')

@app.route('/home',methods=['GET','POST'])
def home():
    if g.user:
        return render_template('home.html')
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

@app.route('/tweets')
def tweets():
    if g.user:
        return render_template('tweets.html')
    return redirect('login')

@app.route('/sentiment')
def sentiment():
    if g.user:
        form = ModelForm()
        return render_template('sentiment.html',form=form)
    return redirect('login')

@app.errorhandler(Exception)
def handle_error(e):
    return render_template('errors-404.html')

