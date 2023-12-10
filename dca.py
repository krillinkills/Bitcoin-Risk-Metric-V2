import pandas as pd
import numpy as np
import datetime
import yfinance as yf


def dca_simulation(initial_investment, monthly_investment, frequency, prices):
    """
    Simulate Dollar-Cost Averaging (DCA) strategy.

    Parameters:
    - initial_investment: Initial investment amount.
    - monthly_investment: Amount invested per month.
    - frequency: 'monthly' or 'weekly'.
    - prices: Historical prices of the asset.
    """
    # Assuming prices is a pandas DataFrame with a 'Date' column and a 'Price' column
    prices['Date'] = pd.to_datetime(prices['Date'])
    prices.set_index('Date', inplace=True)

    # Resample prices based on frequency
    if frequency == 'monthly':
        prices = prices.resample('M').last()
    elif frequency == 'weekly':
        prices = prices.resample('W').last()
    else:
        raise ValueError("Invalid frequency. Choose 'monthly' or 'weekly'.")

    # Initialize variables
    investment_value = initial_investment
    units_held = 0
    performance_data = {'Date': [], 'Investment Value': [],
                        'Units Held': [], 'Total Value': []}

    # Simulate DCA
    for date, price in prices.iterrows():
        units_bought = monthly_investment / price['Price']
        units_held += units_bought
        investment_value += monthly_investment
        total_value = units_held * price['Price']

        performance_data['Date'].append(date)
        performance_data['Investment Value'].append(investment_value)
        performance_data['Units Held'].append(units_held)
        performance_data['Total Value'].append(total_value)

    # Create a DataFrame for performance data
    performance_df = pd.DataFrame(performance_data)
    performance_df.set_index('Date', inplace=True)

    # Calculate percentage change
    performance_df['Percentage Change'] = (
        performance_df['Total Value'] - initial_investment) / initial_investment * 100

    return performance_df


def fetch_bitcoin_prices(start_date, end_date):
    # Fetch historical Bitcoin prices from Yahoo Finance
    btc_data = yf.download(tickers='BTC-USD', start=start_date, end=end_date)
    return btc_data[['Close']].reset_index()


# Replace these values with your preferred parameters
start_date = '2022-01-01'
end_date = '2023-10-01'
initial_investment = 0
monthly_investment = 100
investment_frequency = 'weekly'

# Fetch Bitcoin prices
bitcoin_prices = fetch_bitcoin_prices(start_date, end_date)

# Run the simulation
result_df = dca_simulation(
    initial_investment, monthly_investment, investment_frequency, bitcoin_prices)

# Print the result
print(result_df)
