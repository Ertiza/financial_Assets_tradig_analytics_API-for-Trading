from fastapi import FastAPI, HTTPException
import pandas as pd
from db import engine
from data_fetcher import fetch_yfinance_data, fetch_fred_data

app = FastAPI()

@app.get("/data/{table}/{id}")
async def get_data(table: str, id: str, start_date: str = None, end_date: str = None):
    query = f"SELECT * FROM {table} WHERE "
    if table == "market_data":
        query += f"ticker = '{id}'"
    else:
        query += f"series_id = '{id}'"
    if start_date and end_date:
        query += f" AND date BETWEEN '{start_date}' AND '{end_date}'"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@app.post("/fetch/market_data/{ticker}")
async def fetch_and_store_market_data(ticker: str, start_date: str, end_date: str):
    df = fetch_yfinance_data(ticker, start_date, end_date)
    store_data(df, "market_data")
    return {"message": f"Data for {ticker} stored successfully"}

@app.post("/fetch/economic_data/{series_id}")
async def fetch_and_store_economic_data(series_id: str):
    df = fetch_fred_data(series_id)
    store_data(df, "economic_data")
    return {"message": f"Data for {series_id} stored successfully"}