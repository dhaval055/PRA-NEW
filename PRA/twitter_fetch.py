import re
import tweepy as tw
from PRA import twitter_creds
auth = tw.OAuthHandler(twitter_creds.CONSUMER_KEY, twitter_creds.CONSUMER_SECRET)
auth.set_access_token(twitter_creds.ACCESS_TOKEN, twitter_creds.ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def clean_tweet(tweet):
    """cleaning tweets"""
    cleaned_tweet= ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    cleaned_tweet =cleaned_tweet.lower()
    return cleaned_tweet

def followers(username):
    user = api.get_user(username)
    followers = user.followers_count
    return followers

def timeline_tweets(username):
    tweets_data = api.user_timeline(screen_name=username,count=200)
    for i in tweets_data:
        if not i.retweeted:
            cleaned_tweets = [clean_tweet(tweet.text) for tweet in i]
    return cleaned_tweets

def hashtag_tweets(hashtag_list):
    cleaned_tweets =[]
    location = []
    search = tw.Cursor(api.search, q=hashtag_list, lang="en").items(200)
    for i in search:
        if not i.retweeted and 'RT' not in i.text:
            cleaned_tweets.append(clean_tweet(i.text))
            location.append(i.user.location)
    return cleaned_tweets,location


