"""
Houses trading algorithms
"""

from datetime import datetime, date, timedelta, time as datetime_time
from dotenv import load_dotenv, find_dotenv
import logger

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.get_logger()

class SentimentAlgorithm():
    """
    Static class to store tweet sentiment trading algorithm
    Note that tweet data is stored by the monitor streaming application
    """

    BUY_COUNT = 2
    HOLD_COUNT = 5

    @staticmethod
    def execute(trader, data_api):
        """
        Executes trade algorithm
        """

        # TODO: store relevant positions in DB

        yesterday = datetime.combine(
            date.today() - timedelta(days=1),
            datetime_time()
        )

        # get yesterday's sentiments

        sentiments = data_api.get_sentiments_by_date(start=yesterday, end=yesterday)
        tickers_dict = data_api.get_tickers_dict()

        # identify tickers to hold based on best sentiments

        tickers_to_hold = []
        for i in range(SentimentAlgorithm.HOLD_COUNT):
            ticker_id = sentiments[i]['_id']
            tickers_to_hold.append(tickers_dict[ticker_id])

        _logger.info("Tickers to hold: %s", tickers_to_hold)

        # find old positions and sell them if we aren't holding

        prev_positions = data_api.get_positions(tag='S')

        sell_orders = []
        tickers_held = []
        for position in prev_positions:
            if position['symbol'] not in tickers_to_hold:
                sell_orders.append({
                    'symbol': position['symbol'],
                    'qty': position['qty'],
                    'side': 'sell',
                    'type': 'market',
                    'time_in_force': 'day'
                })
            else:
                tickers_held.append(position['symbol'])

        orders = trader.submit_orders(sell_orders)
        trader.await_orders(orders)
        data_api.update_positions(tag='S', orders=sell_orders)

        _logger.info("All sell orders (if any) complete")

        # buy new positions based on sentiments

        buy_orders = []
        for ticker in tickers_to_hold:
            if ticker not in tickers_held:
                buy_orders.append({
                    'symbol': ticker,
                    'qty': SentimentAlgorithm.BUY_COUNT,
                    'side': 'buy',
                    'type': 'market',
                    'time_in_force': 'day'
                })
        _logger.debug(buy_orders)

        orders = trader.submit_orders(buy_orders)
        _logger.debug(orders)
        trader.await_orders(orders)
        data_api.update_positions(tag='S', orders=buy_orders)

        _logger.info("All buy orders (if any) complete")

class HeikinAshiAlgorithm():
    """
    Static class to store Heikin-Ashi trade algorithm
    """

    BUY_COUNT = 2

    @staticmethod
    def execute(trader, data_api):
        """
        Executes trade algorithm
        """

        # identify tickers we care about

        active_tickers = []

        ticker_list = data_api.get_tickers_name()
        for ticker in ticker_list:
            # if ticker not in active_tickers:
            active_tickers.append(ticker)

        active_positions = list(data_api.get_positions(tag='HA'))
        active_position_tickers = []
        active_positions_dict = {}

        for position in active_positions:

            active_position_tickers.append(position['symbol'])
            active_positions_dict[position['symbol']] = position['qty']

            if position['symbol'] not in active_tickers:
                active_tickers.append(position['symbol'])

        # calculate HA data for previous year (always recompute, never store)

        one_year_ago = datetime.combine(
            date.today() - timedelta(days=365),
            datetime_time()
        )

        yesterday = datetime.combine(
            date.today() - timedelta(days=1),
            datetime_time()
        )

        bars = trader.get_bars(
            active_tickers,
            timeframe='day',
            start=str(one_year_ago.timestamp()),
            end=str(yesterday.timestamp())
        )

        _logger.info("got ticker bars")

        ha_calc = {} # store HA in here
        orders = [] # store trades in here
        for ticker in bars:

            # calc HA bars
            ha_calc[ticker] = []
            for index, bar in enumerate(bars[ticker]): # array of Bars
                if index == 0:
                    c = (bar.o + bar.h + bar.l + bar.c) / 4
                    o = (bar.o + bar.c) / 2
                    l = bar.l
                    h = bar.h
                    ha_calc[ticker].append({'c': c, 'o': o, 'l': l, 'h': h})
                else:
                    c = (bar.o + bar.h + bar.l + bar.c) / 4
                    o = (ha_calc[ticker][index - 1]['o'] + ha_calc[ticker][index - 1]['c']) / 2
                    l = min(bar.l, c, o)
                    h = max(bar.h, c, o)
                    ha_calc[ticker].append({'c': c, 'o': o, 'l': l, 'h': h})

            # do we have enough data?

            if len(ha_calc[ticker]) < 2:
                continue

            latest_ha = ha_calc[ticker][-1]
            previous_ha = ha_calc[ticker][-2]

            # calculate long buy booleans

            is_latest_bearish = (latest_ha['o'] > latest_ha['c'])
            is_previous_bearish = (previous_ha['o'] > previous_ha['c'])
            is_longer_candle_body = (
                abs(latest_ha['o'] - latest_ha['c']) >
                abs(previous_ha['o'] - previous_ha['c'])
            )
            is_no_upper_wick = (latest_ha['h'] == latest_ha['o'])

            is_long_buy = (
                is_latest_bearish and
                is_previous_bearish and
                is_longer_candle_body and
                is_no_upper_wick
            )

            # calculate short sell booleans

            is_latest_bullish = not is_latest_bearish
            is_previous_bullish = not is_previous_bearish
            is_no_lower_wick = (latest_ha['l'] == latest_ha['o'])

            is_short_sell = (
                is_latest_bullish and
                is_previous_bullish and
                is_longer_candle_body and
                is_no_lower_wick
            )

            # calculate long sell and short buy booleans

            is_long_sell = (
                is_latest_bullish and
                is_previous_bullish and
                is_no_lower_wick
            )

            is_short_buy = (
                is_latest_bearish and
                is_previous_bearish and
                is_no_upper_wick
            )

            # our algorithm only does long trades

            if is_long_buy:
                orders.append({
                    'symbol': ticker,
                    'qty': HeikinAshiAlgorithm.BUY_COUNT,
                    'side': 'buy',
                    'type': 'market',
                    'time_in_force': 'day'
                })

            if is_long_sell and ticker in active_position_tickers:
                orders.append({
                    'symbol': ticker,
                    'qty': active_positions_dict[ticker],
                    'side': 'sell',
                    'type': 'market',
                    'time_in_force': 'day'
                })

        orders_result = trader.submit_orders(orders)
        _logger.debug(orders)
        trader.await_orders(orders)
        data_api.update_positions(tag='HA', orders=orders)
