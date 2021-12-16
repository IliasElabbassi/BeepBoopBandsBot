# bollinger bands trading bot 
#https://www.investopedia.com/terms/b/bollingerbands.asp
#https://fr.wikipedia.org/wiki/%C3%89cart_type
# https://www.coingecko.com/en/api/documentation

# candles matplotlib https://www.statology.org/matplotlib-python-candlestick-chart/
'''
where:
BOLU=Upper Bollinger Band
BOLD=Lower Bollinger Band
MA=Moving average
TP (typical price)=(High+Low+Close)÷3
n=Number of days in smoothing period (typically 20)
m=Number of standard deviations (typically 2)
σ[TP,n]=Standard Deviation over last n periods of TP
'''

from pycoingecko import CoinGeckoAPI
import time
import utils
import pandas as pd
import sys
import statistics
import numpy as np
from threading import Thread


# global var
VERBOSE = False

# BOLU=MA(TP,n)+m∗σ[TP,n]
# output an array
def BOLU():
    pass

# BOLD=MA(TP,n)−m∗σ[TP,n]
def BOLD():
    pass

# Moving Average during a certain period of time
# take all the prices (high + low + close of a timeframe) during a timeframe and compute its average
# an entry in the output array is equal to a day
def MA(candles):

    c = []

    for arr in candles:
        for ele in arr:
            c.append(ele)

    moving_average = []
    mean_of_each_candle = []
    sum = 0

    for candle in c:
        m = statistics.mean([
            candle.close,
            candle.open,
            candle.high,
            candle.low
            ])

        mean_of_each_candle.append(m)
    
    for i in range(0, 20):
        moving_average.append(mean_of_each_candle[i])

    for i in range(20, len(c)):
        for y in range(20):
            sum += mean_of_each_candle[i-y]
        moving_average.append(sum/20)
        sum = 0

    return np.array(moving_average)

# Standard deviation
def SD(data):
    import math
    return math.stdev(data)


# guide-line :
# connect to coingeko api to get the price
# connect to binance via api to get acces to a market
# create all the functions
# group things together


def getPricesDuringNdays(n):
    cg = CoinGeckoAPI()

    prices = []
    current_ts = time.time() # get current ts
    ts_minus30min = 30*60
    from_ = current_ts-(ts_minus30min*47*n) # 20 days from now
    to_ = current_ts-(ts_minus30min*47*(n-1))
    if VERBOSE:
        print("-----------------GETTING PRICE----------------------")
        print("from_ : {0}".format(time.ctime(from_)))
        print("to_ : {0}".format(time.ctime(to_)))
        print("\n")

    for i in range(1,n-1):
        getted_price = cg.get_coin_market_chart_range_by_id(
                id="terra-luna",
                vs_currency="usd",
                from_timestamp=str(from_), 
                to_timestamp=str(to_)
            )
                    
        prices.append(getted_price)

        from_ = current_ts-(ts_minus30min*47*(n-i))
        to_ = current_ts-(ts_minus30min*47*((n-1)-i))

        if VERBOSE:
            print("from_ : {0}".format(time.ctime(from_)))
            print("to_ : {0}".format(time.ctime(to_)))
            print("\n")


    return prices

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            VERBOSE = True

    prices = getPricesDuringNdays(40)
    candles = []
    opens = []
    closes = []
    highs = []
    lows = []

    for data in prices:
        candles.append(utils.getCandle(data))

    for candle in candles:
        open1, close1, high1, low1 = utils.infoForDataShow(candle)
        opens.append(open1)
        closes.append(close1)
        highs.append(high1)
        lows.append(low1)

    opens = utils.concatenateArrays(opens)
    closes = utils.concatenateArrays(closes)
    highs = utils.concatenateArrays(highs)
    lows = utils.concatenateArrays(lows)


    data = pd.DataFrame({
                        'open': opens,
                        'close': closes,
                        'high': highs,
                        'low': lows
                        }
                        )  

    if VERBOSE:
        print(data)

    ma = MA(candles)

    utils.printChart(data, ma)
    # threads = []
    # threads.append(Thread(target=utils.printChart, args=[data]))
    # threads.append(Thread(target=utils.plotMA, args=[ma]))

    # for thread in threads:
    #     thread.start()  
    #     thread.join()