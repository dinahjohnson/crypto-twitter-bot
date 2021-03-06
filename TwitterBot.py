"""
    Author: Dinah Johnson

"""
from os import environ
from newsapi import NewsApiClient   
import datetime
import time
import tweepy

my_api_key = environ['my_api_key']
ACCESS_SECRET = environ['ACCESS_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET= environ['CONSUMER_SECRET']

today = datetime.date.today()
news_api = NewsApiClient(api_key=my_api_key) 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
error_tweet = "Uh oh @cybergirldinah something went wrong! Please get me back up and running soon."
 
def fetch():
    try:
        data = news_api.get_everything(q='cryptocurrency',from_param=today,
                                to=today,language='en',
                                sort_by='relevancy',
                                page_size=40)
        return data['articles']
    except:
        api.update_status(error_tweet)
    
def getList():
    articles = fetch()
    if len(articles) > 0:
        links = [article['url'] for article in articles]
    else:
        api.update_status(error_tweet)
    
    links = list(set(links)) 
    return links

def job():
    tweets = getList()
    for tweet in tweets:
        try: 
            api.update_status(tweet)
        except tweepy.TweepError as error:
            if error.api_code == 187:
                continue
        time.sleep(1800)

job()