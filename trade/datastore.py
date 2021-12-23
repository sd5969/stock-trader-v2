"""
Interface with database
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import logger

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.get_logger()

_MONGODB_USER = os.getenv("SST_DB_USER")
_MONGODB_PASSWORD = os.getenv("SST_DB_PASSWORD")
_MONGODB_URI = os.getenv("SST_DB_URI")

class DataAPI():
    """
    Interface with database
    """

    def __init__(self, positions_table_name='positions'):
        self.client = None
        self.database = None
        self.connected = False
        self.positions_table_name = positions_table_name

    def connect(self):
        """
        Connect to DB
        """

        self.client = MongoClient("mongodb://" + _MONGODB_USER + ":" + _MONGODB_PASSWORD
        + "@" + _MONGODB_URI)
        _logger.info("connection to db successful")
        self.database = self.client['stock-trader-v2']
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

    def get_tickers_name(self):
        """
        Get ticker record's symbols
        """

        tickers = self.get_tickers_dict()

        tickers_names = []
        for ticker in tickers:
            tickers_names.append(tickers[ticker])

        return tickers_names

    def get_tickers_id(self):
        """
        Get ticker records's IDs
        """

        tickers = self.get_tickers_dict()

        tickers_ids = []
        for ticker in tickers:
            tickers_ids.append(ticker)

        return tickers_ids

    def update_positions(self, tag, orders):
        """
        Store order changes to db
        """

        _logger.debug(orders)

        for order in orders:
            if order['success']:
                _logger.debug(self.database[self.positions_table_name].update({
                    'tag': tag,
                    'symbol': order['order'].symbol
                }, {
                    '$inc': {
                        'qty': (1 if order['order'].side == 'buy' else -1) * int(order['order'].qty)
                    }
                }, upsert=True, multi=True))

        # remove empty positions

        self.database[self.positions_table_name].delete_many({
            'qty': 0
        })

    def get_positions(self, tag):
        """
        Gets positions for a specified tag
        """

        return self.database[self.positions_table_name].find({
            'tag': tag
        })

    def reset_positions(self, tag):
        """
        Clears positions table
        """

        self.database[self.positions_table_name].delete_many({
            'tag': tag
        })
