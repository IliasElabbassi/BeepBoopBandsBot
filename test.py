from pandas.tseries.offsets import Minute
from pycoingecko import CoinGeckoAPI
import pandas as pd
import time
import json
import utils
import Candle
import numpy as np


cg = CoinGeckoAPI()

#cg = CoinGeckoAPI()
#price = cg.get_price(ids='terra-luna', vs_currencies='usd')
#print(price)

ts = pd.Timestamp(1999, 2, 10, 10, 30)
ts_minus30min = 30*60
current_ts = time.time() # get curretn ts
#contract = ... # get contract
ts_20days = 60*60*12*20 # twenty days timestamp


# print(ts.timestamp())
# print("30 min timestamp : {0}".format(ts_minus30min))
# print("20 days timestamp : {0}".format(ts_20days))


# gets 5 min prices if between < 1day
# else if gets 1h if between 1 to 90 days
# else gets daily price

prices2 = cg.get_coin_market_chart_range_by_id(
            id="terra-luna",
            vs_currency="usd",
            from_timestamp=str(current_ts-ts_minus30min*47), 
            to_timestamp=str(current_ts)
            )

prices1 = cg.get_coin_market_chart_range_by_id(
            id="terra-luna",
            vs_currency="usd",
            from_timestamp=str((current_ts-ts_minus30min*47)-ts_minus30min*47), 
            to_timestamp=str(current_ts)
            )

#print(len(prices["prices"]))

#luna = cg.get_coin_by_id(id="terra-luna")

#print(json.dumps(prices, indent=4))

'''
with open('result.json', 'w') as fp:
    json.dump(prices,fp)
'''

def format(json_prices):
    prices = []

    for price in json_prices["prices"]:
        prices.append(price[1])
    
    return prices

#print(format(prices))

def getCandle(prices):
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
            max_ = utils.max(list)
            min_ = utils.min(list)

            candle = Candle.Candle(last_, first_, max_, min_)
            candles.append(candle)

    return candles

def infoForDataShow(candles):
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


candles1 = getCandle(prices1)
candles2 = getCandle(prices2)

open1, close1, high1, low1 = infoForDataShow(candles1)

open2, close2, high2, low2 = infoForDataShow(candles2)

data = pd.DataFrame({
                    'open': np.concatenate((open1, open2), axis=None),
                    'close': np.concatenate((close1, close2), axis=None),
                    'high': np.concatenate((high1, high2), axis=None),
                    'low': np.concatenate((low1, low2), axis=None)
                    }
                    )  

print(data)

utils.printChart(data)