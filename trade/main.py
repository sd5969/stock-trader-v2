"""
Code for executing simple trading algorithm
"""

import os
from dotenv import load_dotenv
import logger
from trader import Trader

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

_logger = logger.init_logger(logger.get_logger())

def main():
    """
    Executes all logic
    """

    trader = Trader()

if __name__ == "__main__":
    # calling main function
    main()
