"""
Interface with database
"""

import os
from datetime import datetime, time
from pymongo import MongoClient
from dotenv import load_dotenv
import logger

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

_logger = logger.get_logger()

_MONGODB_USER = os.getenv("SST_DB_USER")
_MONGODB_PASSWORD = os.getenv("SST_DB_PASSWORD")
_MONGODB_URI = os.getenv("SST_DB_URI")

class DataAPI():
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

    def get_sentiments_by_date(self, filter_date):
        """
        Get sentiments for a specific date
        """

        sentiments = self.database['sentiments'].find({
            'date': datetime.combine( \
                filter_date, \
                time() \
            )
        })
        _logger.info("got all sentiment data")

        # tickers_array = []
        # for ticker in tickers:
        #     tickers_array.append(ticker['symbol'])
        #
        # return tickers_array
