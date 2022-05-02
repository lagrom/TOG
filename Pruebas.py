import pandas as pd

t = pd.read_csv('ETHUSDT-trades-2022-03.csv')


# Midprice
# df para calculos
y = orderbook[['timestamp', 'bid_price', 'ask_price']]
spread_bid = y.groupby(y.timestamp, group_keys=False)['bid_price'].max()
spread_ask = y.groupby(y.timestamp, group_keys=False)['ask_price'].min()
result = pd.merge(spread_bid,
                  spread_ask,
                  on='timestamp')
result['mid_price'] = (result['ask_price'] + result['bid_price'])/2
orderbook1 = pd.merge(
    orderbook, result[['mid_price']], on='timestamp')

orderbook1.head()
time_frame = (orderbook1['timestamp'].max() -
              orderbook1['timestamp'].min()).total_seconds()


# Spread
spread_bid = y.groupby(y.timestamp, group_keys=False)['bid_price'].max()
spread_bid

spread_ask = y.groupby(y.timestamp, group_keys=False)['ask_price'].min()
spread_ask

result = pd.merge(spread_bid,
                  spread_ask,
                  on='timestamp')
result['spread'] = result['ask_price'] - result['bid_price']
result['mid_price'] = (result['ask_price'] + result['bid_price'])/2


orderbook1 = pd.merge(
    orderbook, result[['spread', 'mid_price']], on='timestamp')

# VWAP Volume Weighted Average Price

prep = orderbook1.copy()
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

orderbook1 = pd.merge(orderbook1, result_vwap['vwap'], on='timestamp')

orderbook1.shape
