"""
Class to simulate trades without making them
"""

from trader import Trader

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

    def market_is_open(self):
        """
        Overridden. Market is always open in simulator :)
        """

        return True

    def submit_order(self, order):
        """
        Overridden. Submits an order AKA tracks dollars spent and earned
        """

        # TODO track order amounts in vars, should return Order

    def await_orders(self, orders):
        """
        Overridden. No waiting in the simulator :)
        """

        return

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
