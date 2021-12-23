"""
Houses trading algorithms
"""

from datetime import datetime, date, timedelta, time as datetime_time
from dotenv import load_dotenv, find_dotenv
import logger

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
load_dotenv(find_dotenv())

_logger = logger.get_logger()











class RegressionAlgorithm():
    """
    Static class to store regression-based trade algorithm
    """

    BUY_COUNT = 2

    @staticmethod
    def execute(trader, data_api, trading_date):
        """
        Executes trade algorithm
        """

        # identify tickers we care about

        active_tickers = []

        ticker_list = data_api.get_tickers_name()
        for ticker in ticker_list:
            # if ticker not in active_tickers:
            active_tickers.append(ticker)

        active_positions = list(data_api.get_positions(tag='RA'))
        active_position_tickers = []
        active_positions_dict = {}

        for position in active_positions:

            active_position_tickers.append(position['symbol'])
            active_positions_dict[position['symbol']] = position['qty']

            if position['symbol'] not in active_tickers:
                active_tickers.append(position['symbol'])

        # calculate HA data for previous year (always recompute, never store)

        one_year_ago = datetime.combine(
            trading_date - timedelta(days=365),
            datetime_time()
        )

        yesterday = datetime.combine(
            trading_date - timedelta(days=1),
            datetime_time()
        )

        bars = trader.get_bars(
            active_tickers,
            timeframe='day',
            start=one_year_ago,
            end=yesterday
        )

        _logger.info("got ticker bars for %s to %s", one_year_ago, yesterday)

        ha_calc = {} # store HA in here
        orders = [] # store trades in here
        for ticker in bars:

            # calc HA bars
            ha_calc[ticker] = []
            for index, bar in enumerate(bars[ticker]): # array of Bars
                # _logger.debug("Ticker: %s, Bar date %s", ticker, bar.t)
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

            # _logger.debug("Latest HA values for ticker %s are %s", ticker, latest_ha)
            # _logger.debug("Length of HA array is %d", len(ha_calc[ticker]))

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
                _logger.debug(
                    "Long buy found for %s (stock currently %s)",
                    ticker,
                    ("held" if ticker in active_position_tickers else "not held")
                )

                if ticker not in active_position_tickers:
                    orders.append({
                        'symbol': ticker,
                        'qty': HeikinAshiAlgorithm.BUY_COUNT,
                        'side': 'buy',
                        'type': 'market',
                        'time_in_force': 'day'
                    })

            if is_long_sell:
                _logger.debug(
                    "Long sell found for %s (stock currently %s)",
                    ticker,
                    ("held" if ticker in active_position_tickers else "not held")
                )

                if ticker in active_position_tickers:
                    orders.append({
                        'symbol': ticker,
                        'qty': active_positions_dict[ticker],
                        'side': 'sell',
                        'type': 'market',
                        'time_in_force': 'day'
                    })

        orders_result = trader.submit_orders(orders)
        # _logger.debug(orders)
        trader.await_orders(orders_result.copy())
        data_api.update_positions(tag='HA', orders=orders_result)

        _logger.info("All HA trades (if any) complete")
