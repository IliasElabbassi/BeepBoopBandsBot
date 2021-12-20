# bollinger bands trading bot 
#https://www.investopedia.com/terms/b/bollingerbands.asp
#https://fr.wikipedia.org/wiki/%C3%89cart_type
# https://www.coingecko.com/en/api/documentation
# https://cryptorank.io/api

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
from binance.client import Client

# global var
VERBOSE = False
M = 2    # number of standard deviation

# BOLU=MA(TP,n)+m∗σ[TP,n]
# output an array
def BOLU(ma, std_dev):
    if VERBOSE:
        print("------computing Bolling Upper Band-------------")
    bolu_ = []

    for i in range(0,len(std_dev)):
        bolu_.append(ma[i] + (M*std_dev[i]))

    return bolu_

# BOLD=MA(TP,n)−m∗σ[TP,n]
def BOLD(ma, std_dev):
    if VERBOSE:
        print("------computing Bolling Lower Band-------------")
    bold_ = []

    for i in range(0,len(std_dev)):
        bold_.append(ma[i] - (M*std_dev[i]))

    return bold_

def computeAllSD(ma):
    if VERBOSE:
        print("------computing moving average standard deviation -------------")
    std_dev =  []
    for price in ma:
        std_dev.append(SD(price))

    return std_dev

# Moving Average during a certain period of time
# take all the prices (high + low + close of a timeframe) during a timeframe and compute its average
# an entry in the output array is equal to a day (with the coingeko api)
# an entry in the output array is equal to 30min (with the binance api)
def MA(candles):
    if VERBOSE:
        print("------computing moving average -------------")

    # c = []

    # for arr in candles:
    #     for ele in arr:
    #         c.append(ele)

    moving_average = []
    mean_of_each_candle = []
    sum = 0
    
    # for candle in c:
    for candle in candles:
        m = statistics.mean([
            candle.close,
            candle.open,
            candle.high,
            candle.low
            ])

        mean_of_each_candle.append(m)
    
    for i in range(0, 20):
        moving_average.append(mean_of_each_candle[i])

    # for i in range(20, len(c)):
    for i in range(20, len(candles)):
        for y in range(20):
            sum += mean_of_each_candle[i-y]
        moving_average.append(sum/20)
        sum = 0

    return moving_average


# Standard deviation
def SD(data):
    return statistics.stdev(data)
    

def realSD(ma):
    sd = []
    temp = np.array(ma)
    for i in range(20, len(temp)):
        sd.append(SD(temp[i-20:i]))

    return sd

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

def get_price_from_Binance():    
    API_KEY = # your binance api key here
    SECRET = # your binance secret key here

    client = Client(API_KEY, SECRET)

    klines = client.get_historical_klines("LUNAUSDT", client.KLINE_INTERVAL_1MINUTE, "10 November 2021")

    df = pd.DataFrame(klines, 
            columns=[
                'timestamp',
                'open',
                'high',
                'low',
                'close',
                'volume',
                'close_time',
                'quote_av',
                'trades',
                'tb_base_av',
                'tb_quote_av',
                'ignore'
            ]
    )

    del df['ignore']
    del df['close_time']
    del df['tb_quote_av']
    del df['tb_base_av']
    del df['trades']
    del df['quote_av']

    df['close'] = pd.to_numeric(df['close'])
    df['low'] = pd.to_numeric(df['low'])
    df['high'] = pd.to_numeric(df['high'])
    df['open'] = pd.to_numeric(df['open'])

    df.set_index(df['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')

    del df['timestamp']

    return df

if __name__ == "__main__":

    for arg in sys.argv:
        if arg == "-v":
            VERBOSE == True
        
    # prices = getPricesDuringNdays(40)
    # candles = []
    # opens = []
    # closes = []
    # highs = []
    # lows = []

    data = get_price_from_Binance()

    candles = utils.getCandle_binance(data)


    # for data in prices:
    #     candles.append(utils.getCandle(data))

    # for candle in candles:
    #     open1, close1, high1, low1 = utils.infoForDataShow(candle)
    #     opens.append(open1)
    #     closes.append(close1)
    #     highs.append(high1)
    #     lows.append(low1)

    # opens = utils.concatenateArrays(opens)
    # closes = utils.concatenateArrays(closes)
    # highs = utils.concatenateArrays(highs)
    # lows = utils.concatenateArrays(lows)


    opens, closes, highs, lows = utils.infoForDataShow(candles)



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

    for m in ma:
        print(m)

    std_dev = realSD(ma)

    sub_ma = np.array(ma)
    sub_ma = sub_ma[19:-1]
    ma = np.array(ma)

    BU = np.array(BOLU(sub_ma, std_dev))
    BD = np.array(BOLD(sub_ma, std_dev))

    # zeros = np.zeros(19)
    # zeros = np.zeros(len(ma))
    fill = np.empty(19)
    fill.fill(60)

    BU = np.concatenate((fill, BU), axis=None)
    BD = np.concatenate((fill, BD), axis=None)

    utils.printChart(data, ma, BU, BD)
    # utils.printChart(data, ma, [], [])
