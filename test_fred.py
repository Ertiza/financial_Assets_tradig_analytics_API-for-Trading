from fredapi import Fred
from config import FRED_API_KEY

def test_fred_api():
    try:
        fred = Fred(api_key=FRED_API_KEY)
        data = fred.get_series('GDP')  # Fetch GDP data as a test
        print("FRED API key is working! Sample data:")
        print(data.head())  # Print the first few rows of the data
    except Exception as e:
        print(f"Error with FRED API: {e}")

if __name__ == "__main__":
    test_fred_api()