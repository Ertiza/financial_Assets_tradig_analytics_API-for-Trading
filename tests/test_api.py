import pytest
from db import engine

def test_db_connection():
    assert engine is not None