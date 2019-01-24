"""
Code for executing simple trading algorithm
"""

import os
from datetime import datetime, date, timedelta, time as datetime_time
import time
from dotenv import load_dotenv, find_dotenv
import logger
from trader import Trader
from datastore import DataAPI

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.init_logger(logger.get_logger())
LOOP_WAIT_TIME = 5 # seconds
BUY_COUNT = 2 # number of shares to buy

def await_orders(trader, orders):
    """
    Checks for and waits until all orders passed in are filled
    """

    all_orders_complete = (not orders)

    while not all_orders_complete:
        time.sleep(LOOP_WAIT_TIME)

        orders_statuses = trader.get_orders_status(orders)
        orders_complete = []
        for status in orders_statuses:
            if status['status'] in ['filled']:
                orders_complete.append(status['order_id'])

        for index, order in reversed(list(enumerate(orders))):
            if order.id in orders_complete:
                orders.pop(index)

        all_orders_complete = (not orders)

def main():
    """
    Executes all logic
    """

    trader = Trader()
    data_api = DataAPI()
    data_api.connect()

    yesterday = datetime.combine( \
        date.today() - timedelta(days=1), \
        datetime_time() \
    )

    sentiments = data_api.get_sentiments_by_date(start=yesterday, end=yesterday)
    tickers_dict = data_api.get_tickers_dict()

    tickers_to_hold = []
    for i in range(5):
        ticker_id = sentiments[i]['_id']
        tickers_to_hold.append(tickers_dict[ticker_id])

    _logger.info("Tickers to hold: %s", tickers_to_hold)

    prev_positions = trader.get_positions()

    sell_orders = []
    for position in prev_positions:
        if position.symbol not in tickers_to_hold:
            sell_orders.append({
                'symbol': position.symbol,
                'qty': position.qty,
                'side': 'sell',
                'type': 'market',
                'time_in_force': 'day'
            })

    orders = trader.submit_orders(sell_orders)
    await_orders(trader, orders)

    _logger.info("All sell orders (if any) complete")

    buy_orders = []
    for ticker in tickers_to_hold:
        buy_orders.append({
            'symbol': ticker,
            'qty': BUY_COUNT,
            'side': 'buy',
            'type': 'market',
            'time_in_force': 'day'
        })
    _logger.debug(buy_orders)

    orders = trader.submit_orders(buy_orders)
    _logger.debug(orders)
    await_orders(trader, orders)

    _logger.info("All buy orders (if any) complete")

    # get previous days' sentiment data, calculated avg sentiment and sorted
    # sell all positions from previous day that aren't in top 5 highest sentiment
    # after positions successfully sell:
    # buy top 5 stocks from previous day that aren't already owned
    # done

if __name__ == "__main__":
    # calling main function
    main()
