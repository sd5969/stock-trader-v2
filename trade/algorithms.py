"""
Houses trading algorithms
"""

from datetime import datetime, date, timedelta, time as datetime_time
from dotenv import load_dotenv, find_dotenv
import logger

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.get_logger()

class SentimentAlgorithm():
    """
    Static class to store tweet sentiment trading algorithm
    Note that tweet data is stored by the monitor streaming application
    """

    BUY_COUNT = 2
    HOLD_COUNT = 5

    @staticmethod
    def execute(trader, data_api):
        """
        Executes trade algorithm
        """

        # TODO: store relevant positions in DB

        yesterday = datetime.combine( \
            date.today() - timedelta(days=1), \
            datetime_time() \
        )

        sentiments = data_api.get_sentiments_by_date(start=yesterday, end=yesterday)
        tickers_dict = data_api.get_tickers_dict()

        tickers_to_hold = []
        for i in range(SentimentAlgorithm.HOLD_COUNT):
            ticker_id = sentiments[i]['_id']
            tickers_to_hold.append(tickers_dict[ticker_id])

        _logger.info("Tickers to hold: %s", tickers_to_hold)

        prev_positions = trader.get_positions()

        sell_orders = []
        tickers_held = []
        for position in prev_positions:
            if position.symbol not in tickers_to_hold:
                sell_orders.append({
                    'symbol': position.symbol,
                    'qty': position.qty,
                    'side': 'sell',
                    'type': 'market',
                    'time_in_force': 'day'
                })
            else:
                tickers_held.append(position.symbol)

        orders = trader.submit_orders(sell_orders)
        trader.await_orders(orders)
        data_api.update_positions(tag='S', orders=sell_orders)

        _logger.info("All sell orders (if any) complete")

        buy_orders = []
        for ticker in tickers_to_hold:
            if ticker not in tickers_held:
                buy_orders.append({
                    'symbol': ticker,
                    'qty': SentimentAlgorithm.BUY_COUNT,
                    'side': 'buy',
                    'type': 'market',
                    'time_in_force': 'day'
                })
        _logger.debug(buy_orders)

        orders = trader.submit_orders(buy_orders)
        _logger.debug(orders)
        trader.await_orders(orders)
        data_api.update_positions(tag='S', orders=buy_orders)

        _logger.info("All buy orders (if any) complete")

class HeikinAshiAlgorithm():
    """
    Static class to store Heikin-Ashi trade algorithm
    """

    @staticmethod
    def execute(trader, data_api):
        """
        Executes trade algorithm
        """

        # set up HA data, likely use past 1 year's data for (active tickers + active HA positions)
        #

        pass
