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
def MA(n):
    pass

# Standard deviation
def SD():
    pass


# guide-line :
# connect to coingeko api to get the price
# connect to binance via api to get acces to a market
# create all the functions
# group things together


def getPricesDuring20days():
    cg = CoinGeckoAPI()

    prices = []
    current_ts = time.time() # get current ts
    ts_minus30min = 30*60
    from_ = current_ts-(ts_minus30min*47*20) # 20 days from now
    to_ = current_ts-(ts_minus30min*47*19)
    if VERBOSE:
        print("-----------------GETTING PRICE----------------------")
        print("from_ : {0}".format(time.ctime(from_)))
        print("to_ : {0}".format(time.ctime(to_)))
        print("\n")

    for i in range(1,19):
        getted_price = cg.get_coin_market_chart_range_by_id(
                id="terra-luna",
                vs_currency="usd",
                from_timestamp=str(from_), 
                to_timestamp=str(to_)
            )
                    
        prices.append(getted_price)

        from_ = current_ts-(ts_minus30min*47*(20-i))
        to_ = current_ts-(ts_minus30min*47*(19-i))

        if VERBOSE:
            print("from_ : {0}".format(time.ctime(from_)))
            print("to_ : {0}".format(time.ctime(to_)))
            print("\n")


    return prices

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            VERBOSE = True

    prices = getPricesDuring20days()
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

    utils.printChart(data)