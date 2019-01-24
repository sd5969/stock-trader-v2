"""
Reusable logging functions
"""

import logging
import sys

def get_logger():
    """
    Returns logger for use
    """
    return logging.getLogger("sentiment-stock-trader")

def init_logger(logger):
    """
    Sets up logger
    """
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(stream=sys.stdout) # pylint: disable=invalid-name
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
