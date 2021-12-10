from pandas.tseries.offsets import Minute
from pycoingecko import CoinGeckoAPI
import pandas as pd
import time

#cg = CoinGeckoAPI()
#price = cg.get_price(ids='terra-luna', vs_currencies='usd')
#print(price)

ts = pd.Timestamp(1999, 2, 10, 10, 30)
ts_minus30min = 30*60
current_ts = time.time()# get curretn ts
contract = ... # get contract

print(ts.timestamp())
print("30 min timestamp : {0}".format(ts_minus30min))


price = cg.get_coin_market_chart_range_by_id(
            ids="terra-luna",
            vs_currencies="usd",
            contract_address=contract,
            from=current_ts-ts_minus30min,
            to=current_ts
            )