import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import chart_studio.plotly as py
from IPython.display import display
import time
import sys
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn import datasets
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from statsmodels.tsa.arima.model import ARIMA


orderbook = pd.read_parquet('orderbook_1hour.parquet')


# Reviso la distribucion de los datos
orderbook.describe()

# Verifico si hay NaN
orderbook.isna().sum()

f, axes = plt.subplots(1, 2, figsize=(18, 12), dpi=50, sharex=True)
plt.suptitle(
    'Comparativo de distribución de datos en volumenes y precios', fontsize=22)
sns.boxplot(data=orderbook[['ask_vol', 'bid_vol']],
            ax=axes[0]).set(ylim=(0, 10))
sns.boxplot(data=orderbook[['ask_price', 'bid_price']], ax=axes[1])
plt.show()


# Resampling

orderbook = orderbook.set_index('timestamp')

data_ask = orderbook['ask_price'].resample('S').ohlc()
data_ask.isna().sum()
data_ask.fillna(method='ffill', inplace=True)
data_ask.isna().sum()
# data_ask[(data_ask.open==False)]

data_bid = orderbook['bid_price'].resample('S').ohlc()
data_bid.isna().sum()
data_bid.fillna(method='ffill', inplace=True)
data_bid.isna().sum()
# data_bid[(data_bid.open==False)]


vol = orderbook[['bid_vol', 'ask_vol']].resample('S').sum()
vol.isna().sum()
vol[vol['bid_vol'] == 0].count()
vol.replace(to_replace=0, method='ffill', inplace=True)
vol[vol['bid_vol'] == 0].count()

data_ask_bid = pd.concat([data_ask, data_bid, vol],
                         axis=1, keys=['Ask', 'Bid', 'Volume'])

# Verifico si hay datos vacios
data_ask_bid.isna().sum()

data_ask_bid.head()
data_ask_bid.keys()

# Target
data_ask_bid['Target'] = data_ask_bid[(
    'Ask', 'close')] - data_ask_bid[('Ask', 'open')]

# Features

# MidPrice
data_ask_bid['mid_price'] = (
    data_ask_bid[('Bid', 'high')] + data_ask_bid[('Ask', 'low')])/2

# Spread
data_ask_bid['spread'] = abs(
    (data_ask_bid[('Bid', 'high')] - data_ask_bid[('Ask', 'low')]))

# Volume Imbalance
data_ask_bid['Vol_Imbalance'] = abs(
    data_ask_bid[('Volume', 'bid_vol')] - data_ask_bid[('Volume', 'ask_vol')])

# Weighted mid price
data_ask_bid['Wghtd_mid_price'] = ((data_ask_bid[('Ask', 'low')]*data_ask_bid[('Volume', 'bid_vol')]) + (data_ask_bid[(
    'Bid', 'high')]*data_ask_bid[('Volume', 'ask_vol')]))/(data_ask_bid[('Volume', 'bid_vol')] + data_ask_bid[('Volume', 'ask_vol')])

# Volume weighted average price
data_ask_bid['vwap'] = ((data_ask_bid[('Ask', 'low')]*data_ask_bid[('Volume', 'ask_vol')]) + (data_ask_bid[(
    'Bid', 'high')]*data_ask_bid[('Volume', 'bid_vol')]))/(data_ask_bid[('Volume', 'bid_vol')] + data_ask_bid[('Volume', 'ask_vol')])


data_ask_bid.head()
orderbook1 = data_ask_bid.copy()

orderbook1.isna().sum()

orderbook1[('Volume', 'ask_vol')].sort_values()

orderbook1.shape

orderbook1['Target'].describe()


f, axes = plt.subplots(3, 1, figsize=(18, 12), dpi=50, sharex=True)
plt.suptitle(
    '  ', fontsize=22)

orderbook2 = orderbook1[[('Ask', 'high'), ('Bid', 'low'), ('vwap', '')]]
orderbook2.plot(figsize=(15, 6), ax=axes[0])

orderbook1['Target'].plot(figsize=(15, 6), ax=axes[1])

orderbook3 = orderbook1[[('Volume', 'bid_vol'), ('Volume', 'ask_vol')]]
orderbook3.plot(figsize=(15, 6), ax=axes[2])

plt.show()


X = sm.add_constant(orderbook1['mid_price'])
model = sm.OLS(orderbook1[[('Ask', 'high')]], X)
results = model.fit()

print(results.summary())


plt.scatter(orderbook1['mid_price'], orderbook1[[('Ask', 'high')]], alpha=0.3)
y_predict = results.params[0] + results.params[1]*orderbook1['mid_price']
plt.plot(orderbook1['mid_price'], y_predict, linewidth=3, color='r')
plt.xlabel('Mid Price')
plt.ylabel('Ask High')
plt.title('OLS Regression')

plt.show()


X = sm.add_constant(orderbook1['vwap'])
model = sm.OLS(orderbook1[[('Ask', 'close')]], X)
results = model.fit()

print(results.summary())

plt.scatter(orderbook1['vwap'], orderbook1[[('Ask', 'close')]], alpha=0.3)
y_predict = results.params[0] + results.params[1]*orderbook1['vwap']
plt.plot(orderbook1['vwap'], y_predict, linewidth=3, color='k')
plt.xlabel('vwap')
plt.ylabel('ask close')
plt.title('OLS Regression')

plt.show()


corr = orderbook1.corr()
corr

ax = sns.heatmap(
    corr,
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)
plt.show()


adfuller(orderbook1['Target'])

plot_acf(orderbook1['Target'], lags=20)
plt.show()

plot_pacf(orderbook1['Target'], lags=20)
plt.show()


f = plt.figure()
ax1 = f.add_subplot(121)
ax1.set_title("1er orden")
ax1.plot(orderbook1.Target.diff())

ax2 = f.add_subplot(122)
plot_acf(orderbook1.Target.diff().dropna(), ax=ax2)

plt.show()


f = plt.figure()
ax1 = f.add_subplot(121)
ax1.set_title("2do orden")
ax1.plot(orderbook1.Target.diff().diff())

ax2 = f.add_subplot(122)
plot_acf(orderbook1.Target.diff().diff().dropna(), ax=ax2)

plt.show()

arima_model = ARIMA(orderbook1.Target, order=(2, 1, 3))
model = arima_model.fit()
print(model.summary())
