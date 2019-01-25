"""
Code for executing simple trading algorithm
"""

from dotenv import load_dotenv, find_dotenv
import logger
from trader import Trader
from datastore import DataAPI
from algorithms import SentimentAlgorithm, HeikinAshiAlgorithm

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

    # skip all behavior if market is closed
    if not trader.market_is_open():
        _logger.info("Market is closed, no trading will occur")
        return

    SentimentAlgorithm.execute(trader, data_api)

if __name__ == "__main__":
    # calling main function
    main()
