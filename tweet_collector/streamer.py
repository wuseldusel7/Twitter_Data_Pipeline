import tweepy
import credentials
import pymongo 
import json

#import datetime

client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.twitter


class Listener(tweepy.StreamListener):
    def on_data(self, raw_data):

        self.process_data(raw_data)

        tweet_j = json.loads(raw_data)

        # Pull important data from the tweet to store in the database.
        ###tweet_id = tweet_j['id_str']  # The Tweet ID from Twitter in string format
        ###username = tweet_j['user']['screen_name']  # The username of the Tweet author
        ###followers = tweet_j['user']['followers_count']  # The number of followers the Tweet author has
        text = tweet_j['text']  # The entire body of the Tweet
        ###hashtags = tweet_j['entities']['hashtags']  # Any hashtags used in the Tweet
        ###dt = tweet_j['created_at']  # The timestamp of when the Tweet was created
        ###language = tweet_j['lang']  # The language of the Tweet

        # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
        ###created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        ###tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created}
        tweet = {'text':text}
        #logging.critical(tweet)
        db.tweets.insert_one(tweet)

        # Save the refined Tweet data to MongoDB
        #db.tweets.insert_one(tweet) 

        return True

    def process_data(self, raw_data):
        print(raw_data)

    def on_error(self, status_code):
        if status_code == 420:
            return False

class Stream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self, keyword_list):
        self.stream.filter(track=keyword_list)

if __name__ == "__main__":
    listener = Listener()

    auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_KEY_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)
    stream.start(['CR7'])

