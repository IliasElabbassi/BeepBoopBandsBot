def max(list):
    max = list[0]
    for l in list:
        if l > max:
            max = l
    return max

def min(list):
    min = list[0]
    for l in list:
        if l < min:
            min = l
    return min

def getCandle(prices):
    import Candle
    # 30min candles
    # one input in prices == 5 minutes
    # one candle <----> 5 input in the array
    candles = []
    for i in range(0, len(prices["prices"]), 5):
        list = []
        for j in range(0,5):
            if i+j >= len(prices["prices"]):
                break
            list.append(prices["prices"][i+j][1])

        if list:
            first_ = list[0]
            last_ = list[-1]
            max_ = max(list)
            min_ = min(list)

            candle = Candle.Candle(last_, first_, max_, min_)
            candles.append(candle)

    return candles

def format(json_prices):
    prices = []

    for price in json_prices["prices"]:
        prices.append(price[1])
    
    return prices


def infoForDataShow(candles):
    import numpy as np
    open = []
    close = []
    high = []
    low = []
    for candle in candles:
        open.append(candle.open)
        close.append(candle.close)
        high.append(candle.high)
        low.append(candle.low)
    
    return (np.array(open), np.array(close), np.array(high), np.array(low))

def printChart(data):
    import matplotlib.pyplot as plt

    #create figure    
    plt.figure()

    #define width of candlestick elements
    width = .4
    width2 = .05

    #define up and down prices
    up = data[data.close>=data.open]
    down = data[data.close<data.open]

    #define colors to use
    col1 = 'green'
    col2 = 'red'


    #plot up prices
    plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
    plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
    plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)


    #plot down prices
    plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
    plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
    plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)


    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    #display candlestick chart
    plt.show()
