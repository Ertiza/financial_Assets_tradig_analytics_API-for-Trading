import pytest
from data_fetcher import fetch_yfinance_data, fetch_fred_data

def test_fetch_yfinance_data():
    df = fetch_yfinance_data("AAPL", "2023-01-01", "2023-01-10")
    assert not df.empty

def test_fetch_fred_data():
    df = fetch_fred_data("GDP")
    assert not df.empty