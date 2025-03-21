import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_market_data():
    response = client.get("/data/market_data/AAPL")
    assert response.status_code == 200