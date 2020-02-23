from PRA import mongo,app
from PRA.routes import g
import random

def total_tweets():
    query = mongo.db.tweets.count_documents({'User':g.user})
    return query

def positive_count():
    query = mongo.db.tweets.count_documents({'User':g.user,'Tweet.Polarity':'Positive'})
    return query

def negative_count():
    query = mongo.db.tweets.count_documents({'User':g.user,'Tweet.Polarity':'Negative'})
    return query

def wordcloud_data():
    query = mongo.db.tweets.find({'User':g.user},{'_id':0,'Tweet.Text':1})
    words = ''
    words = ' '.join(str(text['Tweet']['Text']) for text in query) 
    words = words.split(' ')         
    words = random.choices(words,k=50)
    return words

def wordcloud_data_neg():
    query = mongo.db.tweets.find({'User':g.user,'Tweet.Polarity':'Negative'},{'_id':0,'Tweet.Text':1})
    words = ''
    words = ' '.join(str(text['Tweet']['Text']) for text in query) 
    words = words.split(' ')         
    words = random.choices(words,k=50)
    return words

def tweets_location():
        query = mongo.db.tweets.find({'User':g.user},{'_id':0,'Tweet.Location':1}).limit(7)
        location = [str(i.get("Tweet").get("Location","N/A")) for i in query]
        return location

