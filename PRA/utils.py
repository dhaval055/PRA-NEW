import pickle
import nltk 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 
import re
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

sentiment_model = pickle.load(open('PRA/ml_models/LR_clf.sav','rb'))
# sentiment_model contains logistic regression classifier trained on 100k tweets with 74% accuracy as of now

def clean_tweet(tweet):
    """cleaning tweets"""
    cleaned_tweet= ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    cleaned_tweet =cleaned_tweet.lower()
    return cleaned_tweet

def process_tweet(tweet):
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(w,pos='v') for w in w_tokenizer.tokenize(tweet)]
    return ' '.join(str(i) for i in lemmatized)

def tweet_wrapper(tweet):
    """wrapper function for clean_tweet & process_tweet"""
    cleaned_tweet = clean_tweet(tweet)
    return process_tweet(cleaned_tweet)

def sentiment_score(text):
    """ takes text as input and computes confidence"""
    polarity = ''
    score = sentiment_model.predict_proba([text])
    if score[0][0] > score[0][1]:
        return [text,'Negative',score[0][0]]
    if score[0][1] >= score[0][0]:
        return [text,'Positive',score[0][1]]

def extract_ne(text):
    """ takes text as input and performs NER """
    docx = nlp(text)
    html = displacy.render(docx,style="ent")
    html = html.replace("\n\n","\n")
    return html
