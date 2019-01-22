"""
Parses streaming tweets
"""

import os
from threading import Thread
import tweepy
from dotenv import load_dotenv
from classifier import TweetClassifier
import logger

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

_logger = logger.init_logger(logger.get_logger())

class TweetStreamListener(tweepy.StreamListener):
    """
    Listener for tweets
    """

    def on_status(self, status):
        sentiment_score = TweetClassifier.get_tweet_sentiment(status.text)
        _logger.debug(("%1.3f " + status.text), sentiment_score)

class TweetAPI(object):
    """
    Auth for Twitter
    """

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = os.getenv('SST_CONSUMER_KEY')
        consumer_secret = os.getenv('SST_CONSUMER_SECRET')
        access_token = os.getenv('SST_ACCESS_TOKEN')
        access_token_secret = os.getenv('SST_ACCESS_TOKEN_SECRET')

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except Exception as ex:
            _logger.error("Error: Authentication Failed..." + str(ex))

class TweetStream(object):
    """
    Wrapper for threaded streaming
    """

    def __init__(self):
        self.running = False
        self.thread = None
        self.stream = None

    def _start(self):
        api = TweetAPI()

        stream_listener = TweetStreamListener()
        self.stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        self.stream.filter(track=['AAPL', 'NFLX']) # TODO: get this from database

    def start(self):
        """
        Begin streaming
        """
        self.thread = Thread(target=self._start)
        self.thread.daemon = True
        self.running = True
        self.thread.start()

    def stop(self):
        """
        End streaming
        """
        self.running = False
        self.stream.disconnect()
        # self.thread.join()
