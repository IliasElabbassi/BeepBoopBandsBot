from pandas.tseries.offsets import Minute
from pycoingecko import CoinGeckoAPI
import pandas as pd
import time
import json
import utils
import Candle
import numpy as np


cg = CoinGeckoAPI()

ts_minus30min = 30*60
current_ts = time.time() # get curretn ts


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


with open('result.prices1.json', 'w') as fp:
    json.dump(prices1,fp)

with open('result.prices2.json', 'w') as fp:
    json.dump(prices2,fp)


candles1 = utils.getCandle(prices1)
candles2 = utils.getCandle(prices2)

open1, close1, high1, low1 = utils.infoForDataShow(candles1)

open2, close2, high2, low2 = utils.infoForDataShow(candles2)

data = pd.DataFrame({
                    'open': np.concatenate((open1, open2), axis=None),
                    'close': np.concatenate((close1, close2), axis=None),
                    'high': np.concatenate((high1, high2), axis=None),
                    'low': np.concatenate((low1, low2), axis=None)
                    }
                    )  


print(data)

utils.printChart(data)