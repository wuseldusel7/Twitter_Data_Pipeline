import tweepy
import pymongo


client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.twitter

API_KEY = "I5aF2mTt4TIJtsmkBx13XY7s7"
API_SECRET = "zh1bAuMjPDXB9kO5qwhZV54UhveNJbb7xmdLLWf4ERUpc8vpqw"
ACCESS_TOKEN = "1453668913045286913-5SIlJhAMPLfbQ1PtPHpi1CieKU4V6m"
ACCESS_TOKEN_SECRET = "kEAhoF0FttjVDFB2X1aT7KHWbIGqniogQNI2Sil4slIeA"

def get_auth_handler():
    """
    Function for handling Twitter Authentication. See course material for 
    instructions on getting your own Twitter credentials.
    """
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


class MaxTweetsListener(tweepy.StreamListener):

    def __init__(self, max_tweets, *args, **kwargs):
        # initialize the StreamListener
        super().__init__(*args, **kwargs)
        # set the instance attributes
        self.max_tweets = max_tweets
        self.counter = 0

    def on_connect(self):
        print('connected. listening for incoming tweets')

    def on_status(self, status):
        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        # increase the counter
        self.counter += 1

        tweet = {
            'text': status.text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count
        }

        print(f'New tweet arrived: {tweet["text"]}')

        db.tweets.insert_one(tweet)

        # check if we have enough tweets collected
        if self.max_tweets == self.counter:
            # reset the counter
            self.counter = 0
            # return False to stop the listener
            return False

    def on_error(self, status):
        if status == 420:
            print(f'Rate limit applies. Stop the stream.')
            return False


if __name__ == '__main__':
    auth = get_auth_handler()
    listener = MaxTweetsListener(max_tweets=20)
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['musk'], languages=['en'], is_async=False)
    