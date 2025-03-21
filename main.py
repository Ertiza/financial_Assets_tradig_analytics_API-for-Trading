from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from datetime import datetime
import pandas as pd
import logging
from db import engine, store_data
from data_fetcher import fetch_yfinance_data, fetch_fred_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api.log"),  # Log to a file
        logging.StreamHandler()         # Log to the console
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Helper function to validate date format
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        logger.error(f"Invalid date format: {date_str}")
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

# Endpoint to fetch and store stock market data
@app.post("/fetch/market_data/{ticker}")
async def fetch_and_store_market_data(
    ticker: str,
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    background_tasks: BackgroundTasks = None
):
    logger.info(f"Received request to fetch market data for {ticker} from {start_date} to {end_date}")

    # Validate dates
    start_date = validate_date(start_date)
    end_date = validate_date(end_date)

    # Fetch data
    df = fetch_yfinance_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if df.empty:
        logger.warning(f"No data found for {ticker} between {start_date} and {end_date}")
        raise HTTPException(status_code=404, detail=f"No data found for {ticker} between {start_date} and {end_date}")

    # Store data
    try:
        if background_tasks:
            # Run storage in the background
            background_tasks.add_task(store_data, df, "market_data")
            logger.info(f"Started background task to store data for {ticker}")
            return {"message": f"Fetching and storing data for {ticker} in the background"}
        else:
            # Run storage synchronously
            store_data(df, "market_data")
            logger.info(f"Data for {ticker} stored successfully")
            return {"message": f"Data for {ticker} stored successfully"}
    except Exception as e:
        logger.error(f"Error storing data for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Error storing data: {str(e)}")

# Endpoint to fetch and store economic data
@app.post("/fetch/economic_data/{series_id}")
async def fetch_and_store_economic_data(
    series_id: str,
    background_tasks: BackgroundTasks = None
):
    logger.info(f"Received request to fetch economic data for {series_id}")

    # Fetch data
    df = fetch_fred_data(series_id)
    if df.empty:
        logger.warning(f"No data found for {series_id}")
        raise HTTPException(status_code=404, detail=f"No data found for {series_id}")

    # Store data
    try:
        if background_tasks:
            # Run storage in the background
            background_tasks.add_task(store_data, df, "economic_data")
            logger.info(f"Started background task to store data for {series_id}")
            return {"message": f"Fetching and storing data for {series_id} in the background"}
        else:
            # Run storage synchronously
            store_data(df, "economic_data")
            logger.info(f"Data for {series_id} stored successfully")
            return {"message": f"Data for {series_id} stored successfully"}
    except Exception as e:
        logger.error(f"Error storing data for {series_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error storing data: {str(e)}")

# Endpoint to retrieve stock market data
@app.get("/data/market_data/{ticker}")
async def get_market_data(
    ticker: str,
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format")
):
    logger.info(f"Received request to retrieve market data for {ticker}")

    # Validate dates if provided
    if start_date:
        start_date = validate_date(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = validate_date(end_date).strftime("%Y-%m-%d")

    # Build query
    query = f"SELECT * FROM market_data WHERE ticker = '{ticker}'"
    if start_date and end_date:
        query += f" AND date BETWEEN '{start_date}' AND '{end_date}'"

    # Fetch data
    df = pd.read_sql(query, engine)
    if df.empty:
        logger.warning(f"No data found for {ticker}")
        raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
    logger.info(f"Retrieved {len(df)} rows of market data for {ticker}")
    return df.to_dict(orient="records")

# Endpoint to retrieve economic data
@app.get("/data/economic_data/{series_id}")
async def get_economic_data(
    series_id: str,
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format")
):
    logger.info(f"Received request to retrieve economic data for {series_id}")

    # Validate dates if provided
    if start_date:
        start_date = validate_date(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = validate_date(end_date).strftime("%Y-%m-%d")

    # Build query
    query = f"SELECT * FROM economic_data WHERE series_id = '{series_id}'"
    if start_date and end_date:
        query += f" AND date BETWEEN '{start_date}' AND '{end_date}'"

    # Fetch data
    df = pd.read_sql(query, engine)
    if df.empty:
        logger.warning(f"No data found for {series_id}")
        raise HTTPException(status_code=404, detail=f"No data found for {series_id}")
    logger.info(f"Retrieved {len(df)} rows of economic data for {series_id}")
    return df.to_dict(orient="records")

# Root endpoint
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Financial Assets Trading API!"}