import yfinance as yf
import pandas as pd
from fredapi import Fred
from config import FRED_API_KEY

# Fetch stock market data from yfinance
def fetch_yfinance_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        df['ticker'] = ticker  # Add ticker column
        df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'ticker']]  # Select relevant columns
        df.index.name = 'date'  # Rename index to 'date'
        df.index = df.index.tz_localize(None)  # Remove timezone information
        return df.dropna()  # Remove rows with missing values
    except Exception as e:
        print(f"Error fetching yfinance data for {ticker}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Fetch economic data from FRED
def fetch_fred_data(series_id):
    try:
        fred = Fred(api_key=FRED_API_KEY)
        data = fred.get_series(series_id)  # Fetch data for the given series ID
        df = pd.DataFrame(data, columns=['value'])  # Convert to DataFrame
        df['series_id'] = series_id  # Add series_id column
        df.index.name = 'date'  # Rename index to 'date'
        return df.dropna()  # Remove rows with missing values
    except Exception as e:
        print(f"Error fetching FRED data for {series_id}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error