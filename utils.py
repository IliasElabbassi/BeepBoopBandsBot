from matplotlib import colors
import math
import pandas as pd

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

def real_min(a,b):
    if a < b:
        return a
    else: return b

def real_max(a,b):
    if a > b:
        return a
    else: return b

def getCandle_binance(df):
    import Candle
    # 30min candles
    # one input in prices == 1 minutes
    # one candle <----> 30 input in the array
    candles = []
    lows = df['low']
    highs = df['high']
    closes = df['close']
    opens = df['open']

    open_set = False

    open_c = None
    close_c = None
    high_c = 0
    low_c = 9999999999


    for i in range(0,len(lows), 30):
        for y in range(0, 30):
            idx = i+y
            if idx >= len(lows)-1:
                high_c = real_max(high_c, highs[idx])
                low_c = real_min(low_c, lows[idx])
                close_c = closes[idx]
                break

            if not open_set:
                open_c = opens[idx]
                open_set = True

            if idx == i+29:
                close_c = closes[idx]

            high_c = real_max(high_c, highs[idx])
            low_c = real_min(low_c, lows[idx])
        
        candle = Candle.Candle(close_c, open_c, high_c, low_c)
        candles.append(candle)
        
        open_c = None
        close_c = None
        high_c = 0
        low_c = 9999999999
        open_set = False
        
    return candles

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

# intervals not quite done
def printChart(data, ma, BU, BD, interval=None):
    import matplotlib.pyplot as plt

    if interval:
        length = len(data['close'])
        f = len(data['close']) - interval

        closes = data['close'][f:length]
        opens = data['open'][f:length]
        highs = data['high'][f:length]
        lows = data['low'][f:length]

        data = pd.DataFrame({
                'open': opens,
                'close': closes,
                'high': highs,
                'low': lows
                }
            )  
        data.reset_index()
        
        ma = ma[f:length]
        BU = BU[f:length]
        BD = BD[f:length]

        print(data)

        print(ma)
        print(BU)
        print(BD)

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
    plt.title("Terra Luna chart")

    # days = []

    # for i in range(1,len(ma)+1):
    #     days.append(i)


    plt.plot(ma, color='r')
    plt.plot(BD, color='b')
    plt.plot(BU, color='b')

    #display candlestick chart
    plt.show()

def plotMA(ma):
    import matplotlib.pyplot as plt

    days = []

    for i in range(1,len(ma)+1):
        days.append(i)

    plt.figure()
    plt.plot(days, ma, color='r')
    plt.xlabel("days")
    plt.ylabel("price")
    plt.title("Moving average")
    plt.show()

def concatenateArrays(arrays):
    import numpy as np
    toReturn = np.concatenate((arrays[0], arrays[1]), axis=None)
    for i in range(2, len(arrays)):
        toReturn = np.concatenate((toReturn, arrays[i]))

    return toReturn
        