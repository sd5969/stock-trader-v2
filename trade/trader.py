"""
Trading interface
"""

import os
from dotenv import load_dotenv, find_dotenv
import alpaca_trade_api as tradeapi
import logger
from exceptions import InsufficientArgumentsError

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.get_logger()

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
            raise InsufficientArgumentsError( \
                "Symbol, Quantity, Side, Type, and Time in Force must be specified." \
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
