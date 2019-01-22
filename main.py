"""Simple tweet classifier"""

import os
import time
import sys
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from dotenv import load_dotenv
from tweetstream import TweetStream
import logger

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

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

    #
    # # calling function to get tweets
    # tweets = api.get_tweets(query='Donald Trump', count=200)
    #
    # # picking positive tweets from tweets
    # ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # # percentage of positive tweets
    # print "Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))
    # # picking negative tweets from tweets
    # ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # # percentage of negative tweets
    # print "Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))
    # # percentage of neutral tweets
    # print "Neutral tweets percentage: {} % \
    #     ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))
    #
    # # printing first 5 positive tweets
    # print "\n\nPositive tweets:"
    # for tweet in ptweets[:10]:
    #     print tweet['text']
    #
    # # printing first 5 negative tweets
    # print "\n\nNegative tweets:"
    # for tweet in ntweets[:10]:
    #     print tweet['text']

if __name__ == "__main__":
    # calling main function
    main()
