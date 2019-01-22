"""
Interface with database
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import logger

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

_logger = logger.get_logger()

_MONGODB_USER = os.getenv("SST_DB_USER")
_MONGODB_PASSWORD = os.getenv("SST_DB_PASSWORD")
_MONGODB_URI = os.getenv("SST_DB_URI")

class DataAPI(object):
    """
    Interface with database
    """

    def __init__(self):
        self.client = None
        self.database = None
        self.connected = False

    def connect(self):
        """
        Connect to DB
        """

        self.client = MongoClient("mongodb://" + _MONGODB_USER + ":" + _MONGODB_PASSWORD \
        + "@" + _MONGODB_URI)
        _logger.info("connection to db successful")
        self.database = self.client['sentiment-stock-trader']
        self.connected = True

    def get_tickers(self):
        """
        Get ticker symbols
        """

        tickers = self.database['tickers'].find({
            'active': True
        })
        _logger.info("got all ticker data")

        tickers_array = []
        for ticker in tickers:
            tickers_array.append(ticker['symbol'])

        return tickers_array

    def store_sentiment(self, sentiment):
        """
        Stores sentiment from tweet
        """

        tickers = self.database['tickers'].find({
            'active': True
        })
        sentiments = self.database['sentiments']

        for ticker in tickers:
            if ticker['symbol'].upper() in sentiment['text'].upper():
                sentiments.update_one({
                    'ticker': ticker['_id'],
                    'date': sentiment['date']
                }, {
                    '$inc': {
                        'count': 1,
                        'sentiment': sentiment['sentiment']
                    }
                }, upsert=True)
