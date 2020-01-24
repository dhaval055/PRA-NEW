""" 
    To use twitter API,import TwitterClient in main project code and instnaciate it with  
    twitter_client = TwitterClient()
    api =twitter_client.get_twitter_client_api()   
    user = api.get_user('USERNAME')
    followers = user.followers_count    
    tweets_data = api.user_timeline(screen_name='realDonaldTrump',count=20)        
"""

from tweepy import OAuthHandler
from tweepy.streaming  import StreamListener
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import re
import twitter_creds

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_creds.CONSUMER_KEY, twitter_creds.CONSUMER_SECRET)
        auth.set_access_token(twitter_creds.ACCESS_TOKEN, twitter_creds.ACCESS_TOKEN_SECRET)
        return auth

class TwitterClient():  
    """fetches tweets from user timeline, takes username and number of tweets as arguments"""
    def __init__(self, user_name=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()  
        self.twitter_client = API(self.auth)
        self.user_name = user_name

    def get_twitter_client_api(self):
        return self.twitter_client    

class TwitterListener(StreamListener):
    """Listener class for printing tweets"""

    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename) as tf:
                tf.write(data)
            return True
        except BaseException as e:
            f"Error on data: {str(e)}"    

    def on_error(self, status):
        if status == 420:
            return False
        print(status)

class TwitterStreamer():
    """class for streaming and processing live tweets """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hashtag_list)

def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

if __name__ == '__main__':
    # hashtag_list = ["Donald trump","hilary clinton","obama"] 
    # fetched_tweets_filename = "tweets.json"
    twitter_client = TwitterClient()
    api =twitter_client.get_twitter_client_api()
    user = api.get_user('realDonaldTrump')
    followers = user.followers_count
    print(followers)
    tweets_data = api.user_timeline(screen_name='realDonaldTrump',count=20)
    cleaned_tweets = [clean_tweet(tweet.text) for tweet in tweets_data]
    print(cleaned_tweets)
       
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)       
