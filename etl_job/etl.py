import logging
import time
#import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from sqlalchemy import create_engine

# Establish a connection to the MongoDB server
client = MongoClient(host="mongodb", port=27017)
# Select the database you want to use withing the MongoDB server
db = client.twitter

docs = db.tweets.find()

time.sleep(10)

pg = create_engine('postgresql://postgres:1234@postgresdb:5432/twitter_db', echo=True)

pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment VARCHAR(500)
);
''')

analyzer = SentimentIntensityAnalyzer()

for doc in docs:
    text = doc['text']
    sentiment = analyzer.polarity_scores(doc['text'])
    score = sentiment['compound']
#    score = 1
    query = "INSERT INTO tweets VALUES (%s, %s);"
    pg.execute(query, (text, score))   


#def transform(exctracted_tweets):
#    ''' Transforms data: clean text, gets sentiment analysis from text, formats date '''
    ## sentiment analysis tomorrow, basically you pass text and get a number between 0-1 as the sentiment score
    ## add the sentiment to the tweet and store in a dataframe or a dictionary
#    transformed_tweets = []
#    for tweet in extracted_tweets:
#        sentiment = 1 # later on you will calculate a sentiment
        # datatype of the tweet: dictionary
#        tweet['sentiment'] = sentiment # adding a key: value pair with 'sentiment' as the key and the score as the value
#        transformed_tweets.append(tweet)
        # transformed_tweets is a list of transformed dictionaries

#    return transformed_tweets


#def load(transformed_tweets):
#    ''' Load final data into postgres'''
    ## example function to load
#    for tweet in transformed_tweets:
#        insert_query = "INSERT INTO tweets VALUES (%s, %s, %s)"
#        pg.execute(insert_query, (tweet['user_name'], tweet['text'], tweet['sentiment']))
#        logging.critical('---Inserted a new tweet into postgres---')
#        logging.critical(tweet)