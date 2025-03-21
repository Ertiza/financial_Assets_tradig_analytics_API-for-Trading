from data_fetcher import fetch_yfinance_data, fetch_fred_data
from db import store_data

# Test fetching and storing yfinance data
def test_yfinance():
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-10-01"
    df = fetch_yfinance_data(ticker, start_date, end_date)
    if not df.empty:
        store_data(df, "market_data")  # No need to pass engine explicitly

# Test fetching and storing FRED data
def test_fred():
    series_id = "GDP"
    df = fetch_fred_data(series_id)
    if not df.empty:
        store_data(df, "economic_data")  # No need to pass engine explicitly

if __name__ == "__main__":
    test_yfinance()
    test_fred()