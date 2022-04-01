
# -- Load base packages
import pandas as pd
import numpy as np
import data as dt
#import nest_asyncio


# nest_asyncio.apply()
# (pending) Get the list of exchanges with the symbol

# Get public trades from the list of exchanges
exchanges = ['binance']
symbol = 'BTC/USDT'

# Fetch realtime orderbook data until timer is out (60 secs is default)
orderbooks = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                           data_type='orderbooks', file_route='Files/OrderBooks', stop_criteria=None,
                           elapsed_secs=10, verbose=2)

# Fetch realtime orderbook data until timer is out (60 secs is default)
publictrades = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                             data_type='publictrades', file_route='files/publictrades', stop_criteria=None,
                             elapsed_secs=10, verbose=2)


def new_nest_dict(m):
    for val in m.values():
        if isinstance(val, dict):
            yield from new_nest_dict(val)
        else:
            yield val


# my_dict={'g':19,'k':32,'z':{'i':89,'q':10,'pa':{'ou':10},'w':6,'h':{'rt':17,'lr':16}}}
b = list(new_nest_dict(orderbooks))
print(b[0])

orderbooks.values()
