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
    prices = []
    current_ts = time.time() # get curretn ts
    ts_minus30min = 30*60

    for i in range(0,20):
        from_ = str(current_ts-(ts_minus30min*47*20)) # 20 days from now
        to_ = str(current_ts-(ts_minus30min*47*19))

        getred_grice = cg.get_coin_market_chart_range_by_id(
                id="terra-luna",
                vs_currency="usd",
                from_timestamp=from_, 
                to_timestamp=to_
            )
        
        prices.append(getred_grice)

    return prices
