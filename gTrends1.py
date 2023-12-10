import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import date
import numpy as np
import pandas as pd
import plotly.express as px
import quandl
import yfinance as yf
import matplotlib.pyplot as plt

# Download historical data from Quandl
df_btc = quandl.get(
    'BCHAIN/MKPRU', api_key='FYzyusVT61Y4w65nFESX').reset_index()

# Convert dates to datetime object for easy use
df_btc['Date'] = pd.to_datetime(df_btc['Date'])

# Sort data by date, just in case
df_btc.sort_values(by='Date', inplace=True)

# Only include data points with existing price
df_btc = df_btc[df_btc['Value'] > 0]

# Get the last price against USD
btcdata = yf.download(tickers='BTC-USD', period='1d', interval='1m')

# Append the latest price data to the dataframe
df_btc.loc[df_btc.index[-1]+1] = [date.today(), btcdata['Close'].iloc[-1]]

# Load Google Trends data
df_trends = pd.read_csv("multiTimeline.csv")

# Normalize Google Trends data to match Bitcoin price scale
df_trends['Normalized_Trends'] = (df_trends['Avg_Searches'] - df_trends['Avg_Searches'].min()) / (
    df_trends['Avg_Searches'].max() - df_trends['Avg_Searches'].min())

# Create a combined dataset with Bitcoin price and normalized Google Trends
df_combined = df_btc.merge(df_trends, on='Date')

# Create a subplots figure
fig = make_subplots(rows=2, cols=1, subplot_titles=[
                    'Bitcoin Market Price', 'Google Trends'])

# Plot Bitcoin market price
fig.add_trace(go.Scatter(x=df_combined['Date'], y=df_combined['Value'],
              mode='lines', name='Bitcoin Price (USD)'), row=1, col=1)

# Plot normalized Google Trends
fig.add_trace(go.Scatter(x=df_combined['Date'], y=df_combined['Normalized_Trends'],
              mode='lines', name='Google Trends (Normalized)'), row=2, col=1)

# Update plot layout
fig.update_layout(
    title='Bitcoin Market Price and Google Trends', xaxis_title='Date')

# Show the plot
fig.show()
