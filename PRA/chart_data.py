from PRA import mongo

def total_tweets():
    query = mongo.db.tweets.count_documents({'User':'dhavaldave055@gmail.com'})
    return query

def positive_count():
    query = mongo.db.tweets.count_documents({'User':'dhavaldave055@gmail.com','Tweet.Polarity':'Positive'})
    return query

def negative_count():
    query = mongo.db.tweets.count_documents({'User':'dhavaldave055@gmail.com','Tweet.Polarity':'Negative'})
    return query

def wordcloud_data():
    query = mongo.db.tweets.find({'User':'dhavaldave055@gmail.com'},{'_id':0,'Tweet.Text':1})
    words = []
    for text in query:
        words.append(text['Tweet']['Text'])    
    return words

