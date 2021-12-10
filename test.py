from pandas.tseries.offsets import Minute
from pycoingecko import CoinGeckoAPI
import pandas as pd
import time
import json
import utils
import Candle

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

prices = cg.get_coin_market_chart_range_by_id(
            id="terra-luna",
            vs_currency="usd",
            from_timestamp=str(current_ts-ts_minus30min*4), 
            to_timestamp=str(current_ts)
            )

#print(len(prices["prices"]))

#luna = cg.get_coin_by_id(id="terra-luna")

#print(json.dumps(prices, indent=4))

with open('result.json', 'w') as fp:
    json.dump(prices,fp)


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
    for i in range(0, len(prices), 5):
        list = []
        for j in range(0,5):
            list.append(prices[i+j])

        first_ = list[0]
        last_ = list[-1]
        max_ = utils.max(list)
        min_ = utils.min(list)

        candle = Candle(last_, first_, max_, min_)
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
    
    return (open, close, high, low)
        

candles = getCandle(prices)

open, close, high, low = infoForDataShow(candles)

data = pd.DataFrame({
                    'open': open,
                    'close': close,
                    'high': high,
                    'low': low
                    })  

print(data)
