from os import close
from binance.client import Client
import pandas as pd
import utils
import matplotlib.pyplot as plt
import numpy as np


API_KEY = # your binance api key here
SECRET = # your binance secret key here

client = Client(API_KEY, SECRET)

klines = client.get_historical_klines("LUNAUSDT", client.KLINE_INTERVAL_1MINUTE, "01 December 2021")

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

print(len(df['close']))
print(len(df['high']))
print(len(df['low']))
print(len(df['open']))

def getCandle(data):
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
                high_c = max(high_c, highs[idx])
                low_c = min(low_c, lows[idx])
                close_c = closes[idx]
                break

            if not open_set:
                open_c = opens[idx]
                open_set = True

            if idx == i+29:
                close_c = closes[idx]

            high_c = max(high_c, highs[idx])
            low_c = min(low_c, lows[idx])
        
        candle = Candle.Candle(close_c, open_c, high_c, low_c)
        candles.append(candle)
        
        open_c = None
        close_c = None
        high_c = 0
        low_c = 9999999999
        open_set = False
        
    return candles

candles = getCandle(df)

for c in candles:
    print("candle : ")
    print("close ", c.close)
    print("open ", c.open)
    print("high ", c.high)
    print("low ", c.low)

opens, closes, highs, lows = utils.infoForDataShow(candles)



data = pd.DataFrame({
                    'open': opens,
                    'close': closes,
                    'high': highs,
                    'low': lows
                    }
                    )

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



#display candlestick chart
plt.show()