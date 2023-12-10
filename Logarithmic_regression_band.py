import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Fetch historical Bitcoin prices
btc_data = yf.download('BTC-USD', start='2015-01-01', end='2023-01-01')

# Create a new column for the natural logarithm of the closing prices
btc_data['Log_Price'] = np.log(btc_data['Close'])

# Convert datetime index to numeric
btc_data['Numeric_Index'] = pd.to_numeric(btc_data.index)

# Fit a linear regression line to the logarithm of prices
coefficients = np.polyfit(btc_data['Numeric_Index'], btc_data['Log_Price'], 1)
line = np.polyval(coefficients, btc_data['Numeric_Index'])

# Create bands based on standard deviations from the regression line
std_dev = np.std(btc_data['Log_Price'] - line)
upper_band = line + 2 * std_dev
lower_band = line - 2 * std_dev

# Plot the Bitcoin prices, regression line, and bands
plt.figure(figsize=(12, 6))
plt.plot(btc_data.index, btc_data['Log_Price'],
         label='Logarithm of Bitcoin Price', color='blue')
plt.plot(btc_data.index, line,
         label='Logarithmic Regression Line', color='orange')
plt.plot(btc_data.index, upper_band, label='Upper Band',
         linestyle='--', color='green')
plt.plot(btc_data.index, lower_band, label='Lower Band',
         linestyle='--', color='red')
plt.legend()
plt.title('Bitcoin Logarithmic Regression Band')
plt.xlabel('Date')
plt.ylabel('Logarithm of Price')
plt.show()
