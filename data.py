"""
Responsible only for:
1. Downloading historical adjusted closing prices using yfinance.
2. Saving the prices to data/stock_prices.csv.
3. Returning the price DataFrame.
4. Computing daily percentage returns.

The CSV format:
Date,AAPL,MSFT,NVDA,...
"""

import os
import pandas as pd
import yfinance as yf

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "stock_prices.csv") # path to the csv file


def fetch_stock_data(symbols, period="2y"):
    """Download historical closing prices and save them to CSV."""

    os.makedirs(DATA_DIR, exist_ok=True) # create the data directory if it doesn't exist

    prices = yf.download(
        tickers=symbols,
        period=period,
        auto_adjust=True, # adjust prices for splits and dividends
        progress=False, # don't show the progress bar
    )["Close"] # get the closing prices

    if isinstance(prices, pd.Series): # isinstance is a built-in function that checks if the object is an instance of the given class, here object is prices and class is pd.Series
        prices = prices.to_frame(name=symbols[0]) # convert the series to a dataframe with the first symbol as the column name

    prices = prices.dropna() # drop rows where all values are NaN, when all tickers are not available for a given date, maybe the market was closed that day
    
    prices.to_csv(CSV_FILE) # save the prices to the csv file

    return prices


def calculate_daily_returns(price_df):
    """Compute daily percentage returns from closing prices."""

    return price_df.pct_change().dropna() # compute the daily percentage returns and drop the rows where the returns are NaN, pct_change is a built-in function that computes the percentage change between the current and previous row of that stock