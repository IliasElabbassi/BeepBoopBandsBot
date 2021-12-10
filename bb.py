# bollinger bands trading bot 
#https://www.investopedia.com/terms/b/bollingerbands.asp
#https://fr.wikipedia.org/wiki/%C3%89cart_type

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

# BOLU=MA(TP,n)+m∗σ[TP,n]
# output an array
def BOLU():
    pass

# BOLD=MA(TP,n)−m∗σ[TP,n]
def BOLD():
    pass

# Moving Average during a certain period of time
# take all the prices (high + low + close of a timeframe) during a day and compute its average
# an entry in the output array is equal to a day
def MA(n):
    pass

# Standard deviation
def SD():
    pass


# guide-line :
# connect to tradingview api to get the price
# connect to binance via api to get acces to a market
# create all the functions
# group things together
