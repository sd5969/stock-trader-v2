"""
Trading interface
"""

import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import logger

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

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
