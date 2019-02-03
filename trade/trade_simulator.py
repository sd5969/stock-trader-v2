"""
Class to simulate trades without making them
"""

from datetime import datetime
from trader import Trader
from exceptions import InvalidOrderError
import logger

_logger = logger.get_logger()

class Order():
    """
    Stubbed order class
    """

    def __init__(self, symbol=None, side=None, qty=None):
        self.symbol = symbol
        self.side = side
        self.qty = qty
        self.status = 'filled'

    @property
    def id(self):
        """
        Returns unique ID for order
        """

        return id(self)

class TradeSimulator(Trader):
    """
    A sub-class of Trader for simulating trades
    """

    def __init__(self):
        super().__init__()
        self.dollars_spent = 0
        self.dollars_earned = 0
        self.trade_time = datetime.now()

    def market_is_open(self):
        """
        Overridden. Market is always open in simulator :)
        """

        return True

    def submit_order(self, order):
        """
        Overridden. Submits an order AKA tracks dollars spent and earned
        """

        response = {
            'success': False,
            'error': None,
            'order': None
        }

        if order['type'] != 'market':
            response['error'] = InvalidOrderError(
                "Simulator only supports market orders"
            )
            return response

        if order['side'] not in ['buy', 'sell']:
            response['error'] = InvalidOrderError(
                "Trade side must be buy or sell"
            )
            return response

        if not isinstance(order['qty'], int) or order['qty'] <= 0:
            response['error'] = InvalidOrderError(
                "Quantity must be a positive integer"
            )
            return response

        bars = self.get_bars(
            tickers=[order['symbol']],
            timeframe='1D',
            start=self.trade_time,
            end=self.trade_time
        )

        if not bars[order['symbol']]:
            response['error'] = InvalidOrderError(
                "Stock data not found for order given"
            )
            return response

        trade_price = (
            bars[order['symbol']][0].o +
            bars[order['symbol']][0].c
        ) / 2 # take average of open and close from that day

        if order['side'] == 'buy':
            self.dollars_spent += order['qty'] * trade_price
        elif order['side'] == 'sell':
            self.dollars_earned += order['qty'] * trade_price

        _logger.debug("Successfully processed order %s %s %s", order['side'], order['qty'], order['symbol'])

        response['success'] = True
        response['order'] = Order(
            symbol=order['symbol'],
            side=order['side'],
            qty=order['qty']
        )

        return response

    def await_orders(self, orders):
        """
        Overridden. No waiting in the simulator :)
        """

        return

    def set_date(self, trade_date):
        """
        Sets simulate trade date
        """

        self.trade_time = trade_date

    def get_profit(self):
        """
        Returns profit
        """

        return self.dollars_earned - self.dollars_spent

    def get_profit_percent(self):
        """
        Returns profit percent on basis
        """

        if self.dollars_spent == 0:
            return 0

        return self.get_profit() / self.dollars_spent
