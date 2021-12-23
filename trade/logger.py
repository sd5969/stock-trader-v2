"""
Reusable logging functions
"""

import logging
import sys

LOG_LEVEL = logging.INFO

def get_logger():
    """
    Returns logger for use
    """
    return logging.getLogger("stock-trader-v2")

def init_logger(logger):
    """
    Sets up logger
    """
    logger.setLevel(LOG_LEVEL)
    ch = logging.StreamHandler(stream=sys.stdout) # pylint: disable=invalid-name
    ch.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
