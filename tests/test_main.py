# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ticker_bad_exchange():
    r = client.get("/ticker/nonexistentsomething/BTC-USDT")
    assert r.status_code == 400 or r.status_code == 502

# we cannot guarantee external exchange responses in CI; for robust tests, mock ccxt calls (advanced)
