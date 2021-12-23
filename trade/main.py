"""
Code for executing simple trading algorithm
"""

from datetime import date
from dotenv import load_dotenv, find_dotenv
import logger
from trader import Trader
from datastore import DataAPI
from algorithms import RegressionAlgorithm

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.init_logger(logger.get_logger())

def main():
    """
    Executes all logic
    """

    trader = Trader()
    data_api = DataAPI()
    data_api.connect()

    # HeikinAshiAlgorithm.execute(trader, data_api)

    # skip all behavior if market is closed
    if not trader.market_is_open():
        _logger.info("Market is closed, no trading will occur")
        return

    RegressionAlgorithm.execute(trader, data_api, date.today())

if __name__ == "__main__":
    # calling main function
    main()
