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

    def get_tickers_dict(self):
        """
        Get dictionary of ticker ID to symbol
        """

        tickers = self.database['tickers'].find({
            'active': True
        })
        _logger.info("got all ticker data")

        tickers_by_id = {}
        for ticker in tickers:
            tickers_by_id[ticker['_id']] = ticker['symbol']

        return tickers_by_id

    def get_tickers_id(self):
        """
        Get ticker records's IDs
        """

        tickers = self.get_tickers_dict()

        tickers_ids = []
        for ticker in tickers:
            tickers_ids.append(ticker)

        return tickers_ids

    def get_sentiments_by_date(self, start, end):
        """
        Get sentiments for a specific date
        """

        tickers = self.get_tickers_id()

        # sentiments = self.database['sentiments'].find({
        #     'date': {
        #         '$gte': start,
        #         '$lte': end
        #     },
        #     'ticker': {
        #         '$in': tickers
        #     }
        # })
        # _logger.info("got all sentiment data for active tickers")

        sentiments = self.database['sentiments'].aggregate([{
            '$match': {
                'date': {
                    '$gte': start,
                    '$lte': end
                },
                'ticker': {
                    '$in': tickers
                }
            }
        }, {
            '$group': {
                '_id': '$ticker',
                'sum_count': {
                    '$sum': '$count'
                },
                'sum_sentiment': {
                    '$sum': '$sentiment'
                }
            }
        }, {
            '$addFields': {
                'average_sentiment': {
                    '$divide': ['$sum_sentiment', '$sum_count']
                }
            }
        }, {
            '$sort': {
                'average_sentiment': -1
            }
        }])
        _logger.info("got all sentiment data for active tickers")


        return list(sentiments)
