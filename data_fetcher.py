import yfinance as yf
import pandas as pd
from fredapi import Fred
from config import FRED_API_KEY

def fetch_yfinance_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    df['ticker'] = ticker
    df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'ticker']]
    df.index.name = 'date'
    return df.dropna()

def fetch_fred_data(series_id):
    fred = Fred(api_key=FRED_API_KEY)
    data = fred.get_series(series_id)
    df = pd.DataFrame(data, columns=['value'])
    df['series_id'] = series_id
    df.index.name = 'date'
    return df.dropna()