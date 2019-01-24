"""Simple tweet classifier"""

import os
import time
import sys
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from dotenv import load_dotenv, find_dotenv
from tweetstream import TweetStream
import logger

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.init_logger(logger.get_logger())

def main():
    """
    Main function that executes threads
    """

    stream = TweetStream()
    stream.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            _logger.info("Shutting down")
            stream.stop()
            sys.exit()

if __name__ == "__main__":
    # calling main function
    main()
