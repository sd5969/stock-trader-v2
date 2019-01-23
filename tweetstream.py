"""
Parses streaming tweets
"""

import os
from datetime import datetime, date, time
from threading import Thread
import tweepy
from dotenv import load_dotenv
from classifier import TweetClassifier
from datastore import DataAPI
import logger

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

_logger = logger.get_logger()

class TweetStreamListener(tweepy.StreamListener):
    """
    Listener for tweets
    """

    def __init__(self, db_interface):
        super(TweetStreamListener, self).__init__()
        self.db_interface = db_interface
        if not self.db_interface.connected:
            self.db_interface.connect()

    def on_status(self, status):
        sentiment_score = TweetClassifier.get_tweet_sentiment(status.text)
        # _logger.debug(("%1.3f " + status.text), sentiment_score)
        _logger.debug("Tweet found, saving sentiment")

        self.db_interface.store_sentiment({
            # 'id': status.id,
            'date': datetime.combine( \
                date.fromtimestamp(int(status.timestamp_ms) / 1000), \
                time() \
            ),
            'text': status.text,
            'sentiment': sentiment_score
        })

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

        db_interface = DataAPI()
        db_interface.connect()
        tickers = map(lambda a: '#' + a, db_interface.get_tickers())

        stream_listener = TweetStreamListener(db_interface=db_interface)
        self.stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        self.stream.filter(languages=['en'], track=tickers)

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
