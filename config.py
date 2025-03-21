from dotenv import load_dotenv
import os

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_DRIVER = os.getenv("SQL_DRIVER")

DATABASE_URL = f"mssql+pyodbc://@{SQL_SERVER}/{SQL_DATABASE}?driver={SQL_DRIVER}&Trusted_Connection=yes"