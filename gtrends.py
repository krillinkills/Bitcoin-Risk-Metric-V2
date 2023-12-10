from datetime import date
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import quandl
import yfinance as yf
import matplotlib.pyplot as plt

# Download historical data from Quandl
df = quandl.get('BCHAIN/MKPRU', api_key='FYzyusVT61Y4w65nFESX').reset_index()

# Convert dates to datetime object for easy use
df['Date'] = pd.to_datetime(df['Date'])

# Sort data by date, just in case
df.sort_values(by='Date', inplace=True)

# Only include data points with existing price
df = df[df['Value'] > 0]

# Get the last price against USD
btcdata = yf.download(tickers='BTC-USD', period='1d', interval='1m')

# Append the latest price data to the dataframe
df.loc[df.index[-1]+1] = [date.today(), btcdata['Close'].iloc[-1]]
df['Date'] = pd.to_datetime(df['Date'])

gTrends = pd.read_csv("multiTimeline.csv")

gTrends["Date"] = gTrends["Category: All categories"].str.split(" ").str[0]

print(gTrends)
plt.figure(figsize=(15, 6))
plt.yscale('log')
plt.plot(df['Date'], df['Value'])
plt.xlabel('Date')
plt.ylabel('Bitcoin Price (USD)')
plt.title('Bitcoin Market Price')
plt.grid(True)
plt.show()
