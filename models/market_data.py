from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MarketData(Base):
    __tablename__ = 'market_data'
    date = Column(DateTime, primary_key=True)
    Open = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Close = Column(Float)
    Volume = Column(Float)
    ticker = Column(String(10))