"""
Code for simulating trading algorithms
"""

import locale
from datetime import datetime, date, timedelta, time as datetime_time
from dotenv import load_dotenv, find_dotenv
import logger
from trade_simulator import TradeSimulator
from datastore import DataAPI
from algorithms import HeikinAshiAlgorithm

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.init_logger(logger.get_logger())
locale.setlocale(locale.LC_ALL, '')

def daterange(date1, date2):
    """
    Function to create date range
    """

    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

START_DATE = date(2018, 12, 3)
END_DATE = date(2018, 12, 24)

def main():
    """
    Executes all logic
    """

    trader = TradeSimulator()
    data_api = DataAPI(positions_table_name='positions_simulated')
    data_api.connect()

    # skip all behavior if market is closed
    if not trader.market_is_open():
        _logger.info("Market is closed, no trading will occur")
        return

    data_api.reset_positions(tag='HA')

    date_range = daterange(START_DATE, END_DATE)
    for date_entry in date_range:
        _logger.info("Simulating Heikin-Ashi on %s", date_entry)
        trader.set_date(
            datetime.combine(
                date_entry,
                datetime_time()
            )
        )
        HeikinAshiAlgorithm.execute(trader, data_api, date_entry)
        _logger.info(
            "Current profit: %s (%d%%)",
            locale.currency(trader.get_profit(), grouping=True),
            (100 * trader.get_profit_percent())
        )

    trader.clear_positions(data_api.get_positions(tag='HA'))

    _logger.info("Date range: %s to %s", START_DATE, END_DATE)
    _logger.info(
        "Total profit: %s (%d%%)",
        locale.currency(trader.get_profit(), grouping=True),
        (100 * trader.get_profit_percent())
    )

    data_api.reset_positions(tag='HA')

if __name__ == "__main__":
    # calling main function
    main()
