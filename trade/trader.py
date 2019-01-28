"""
Trading interface
"""

import os
import time
from dotenv import load_dotenv, find_dotenv
import alpaca_trade_api as tradeapi
import logger
from exceptions import InsufficientArgumentsError

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.get_logger()

LOOP_WAIT_TIME = 5 # seconds
BARS_API_LIMIT = 200

class Trader():
    """
    Trading API interface
    """

    def __init__(self):
        self.api = tradeapi.REST(
            key_id=os.getenv('AL_KEY'),
            secret_key=os.getenv('AL_SECRET'),
            base_url=os.getenv('AL_ENDPOINT')
        )

    def market_is_open(self):
        """
        Returns true if market is open
        """

        return self.api.get_clock().is_open

    def get_positions(self):
        """
        Returns list of all positions
        """

        return self.api.list_positions()

    def submit_order(self, order):
        """
        Submits one order
        """

        if not order['symbol'] or \
            not order['qty'] or \
            not order['side'] or \
            not order['type'] or \
            not order['time_in_force']:
            raise InsufficientArgumentsError(
                "Symbol, Quantity, Side, Type, and Time in Force must be specified."
            )

        return self.api.submit_order(symbol=order['symbol'], \
            qty=order['qty'], \
            side=order['side'], \
            type=order['type'], \
            time_in_force=order['time_in_force'] \
        )

    def submit_orders(self, orders):
        """
        Submits multiple orders via loop
        """

        order_results = []
        for order in orders:
            order_results.append(self.submit_order(order))

        return order_results

    def get_order_status(self, order_id):
        """
        Gets single order status by ID
        """

        return self.api.get_order(order_id).status

    def get_orders_status(self, orders):
        """
        Gets multiple orders' statuses
        """

        statuses = []
        for order in orders:
            statuses.append({
                'order_id': order.id,
                'status': self.get_order_status(order.id)
            })

        return statuses

    def get_open_orders(self):
        """
        Gets all open orders
        """

        orders = self.api.list_orders()

        open_orders = []
        for order in orders:
            if order.status != 'filled':
                open_orders.append(order)

        return open_orders

    def await_orders(self, orders):
        """
        Checks for and waits until all orders passed in are filled
        """

        all_orders_complete = (not orders)

        while not all_orders_complete:
            time.sleep(LOOP_WAIT_TIME)

            orders_statuses = self.get_orders_status(orders)
            orders_complete = []
            for status in orders_statuses:
                if status['status'] in ['filled']:
                    orders_complete.append(status['order_id'])

            for index, order in reversed(list(enumerate(orders))):
                if order.id in orders_complete:
                    orders.pop(index)

            all_orders_complete = (not orders)

    def get_bars(self, tickers, timeframe, start, end):
        """
        Gets bars with specified arguments
        """

        index = 0
        results = {}
        while len(tickers) > index:
            tickers_subset = tickers[index:index + BARS_API_LIMIT]
            results.update(self.api.get_barset(tickers_subset, timeframe, start=start, end=end))
            index += BARS_API_LIMIT

        return results
