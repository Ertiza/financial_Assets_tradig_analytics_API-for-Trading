import pandas as pd  # Add this import statement
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Store data in the database
def store_data(df, table_name, engine=engine):
    try:
        # Check if the table exists
        inspector = inspect(engine)
        if not inspector.has_table(table_name):
            print(f"Table {table_name} does not exist!")
            return

        # Check for existing data
        if table_name == "market_data":
            existing_dates = pd.read_sql(f"SELECT date, ticker FROM {table_name}", engine)
            merge_columns = ['date', 'ticker']
        elif table_name == "economic_data":
            existing_dates = pd.read_sql(f"SELECT date, series_id FROM {table_name}", engine)
            merge_columns = ['date', 'series_id']
        else:
            print(f"Unknown table: {table_name}")
            return

        if not existing_dates.empty:
            # Merge to find new rows
            df = df.merge(existing_dates, on=merge_columns, how='left', indicator=True)
            df = df[df['_merge'] == 'left_only'].drop(columns=['_merge'])

        # Insert new data
        if not df.empty:
            df.to_sql(table_name, engine, if_exists='append', index=False)  # Set index=False to avoid inserting the index column
            print(f"Data stored successfully in {table_name}!")
        else:
            print(f"No new data to store in {table_name}.")
    except Exception as e:
        print(f"Error storing data in {table_name}: {e}")