from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EconomicData(Base):
    __tablename__ = 'economic_data'
    date = Column(DateTime, primary_key=True)
    value = Column(Float)
    series_id = Column(String(20))