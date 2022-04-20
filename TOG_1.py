
import matplotlib.pyplot as plt
import statsmodels.api as sm
from codecs import ignore_errors
import pandas as pd
import numpy as np
import data as dt
import sys
import plotly.graph_objects as go
import chart_studio.plotly as py
from IPython.display import display

#import nest_asyncio


# nest_asyncio.apply()
# (pending) Get the list of exchanges with the symbol

# Get public trades from the list of exchanges
exchanges = ['binance']
symbol = 'BTC/USDT'

# Fetch realtime orderbook data until timer is out (60 secs is default)
orderbooks = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                           data_type='orderbooks', file_route='Files/OrderBooks', stop_criteria=None,
                           elapsed_secs=120, verbose=2)

# Fetch realtime orderbook data until timer is out (60 secs is default)
publictrades = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                             data_type='publictrades', file_route='files/publictrades', stop_criteria=None,
                             elapsed_secs=10, verbose=2)


orderbks = pd.DataFrame()
y = pd.DataFrame()

for key in orderbooks['binance']:
    print(key)
    # print(type(orderbooks['binance'][key]))
    y = orderbooks['binance'][key]
    y['timestamp'] = key
    orderbks = orderbks.append(y, ignore_index=True)
print(orderbks)


# publictrds = pd.DataFrame()

# for key in publictrades['binance']:
#     print(key)
#     print(publictrades['binance'][key])
#     y = publictrades['binance'][key]
#  #   y['key'] = key
#     publictrds = publictrds.append(y)
# print(publictrds)

# publictrds = publictrds.transpose()
# print(publictrds)

# Indexando el orderbook
orderbks.head()

# orderbks.reset_index(drop=True)
orderbks.info()
orderbks.shape

#orderbks['timestamp'].iloc[1] - orderbks['timestamp'].iloc[0]


display(orderbks)

# orderbks.dtypes

#display(orderbks.iloc[0:2, :])


# df para calculos
y = orderbks[['timestamp', 'bid_price', 'ask_price']]


y.head()

# Spread
spread_bid = y.groupby(y.timestamp, group_keys=False)['bid_price'].max()
spread_bid

spread_ask = y.groupby(y.timestamp, group_keys=False)['ask_price'].max()
spread_ask

result = pd.merge(spread_bid,
                  spread_ask,
                  on='timestamp')
result['spread'] = result['ask_price'] - result['bid_price']
result
#result = result.set_index('timestamp')

# mid price

result['mid_price'] = (result['ask_price'] + result['bid_price'])/2

result.head()


# VWAP Volume Weighted Average Price

prep = orderbks
prep['ask_mult'] = prep['ask_vol']*prep['ask_price']
prep['bid_mult'] = prep['bid_vol']*prep['bid_price']
prep['vol_sum'] = prep['ask_vol'] + prep['bid_vol']
prep.head()

first_oper = prep.groupby(prep.timestamp, group_keys=False)['ask_mult'].sum()
sec_oper = prep.groupby(prep.timestamp, group_keys=False)['bid_mult'].sum()
den_oper = prep.groupby(prep.timestamp, group_keys=False)['vol_sum'].sum()

result_vwap = pd.merge(first_oper,
                       sec_oper,
                       on='timestamp')

result_vwap = pd.merge(result_vwap,
                       den_oper,
                       on='timestamp')

result_vwap['vwap'] = (result_vwap['ask_mult'] +
                       result_vwap['bid_mult']) / result_vwap['vol_sum']

result_vwap['vwap']


# Graficas


y = y.set_index('timestamp')
y.plot(figsize=(15, 6))
# plt.show()

y.head()


ts_data_load = y['bid_price']
decomposition = sm.tsa.seasonal_decompose(
    y['bid_price'], period=100, model='additive')

fig = decomposition.plot()
fig.show()
# plt.close(fig)
