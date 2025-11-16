# app/schemas.py
from pydantic import BaseModel
from typing import Any, List

class TickerResponse(BaseModel):
    symbol: str
    datetime: str
    bid: float = None
    ask: float = None
    last: float = None
    info: Any = None

class HistoricalResponse(BaseModel):
    ohlcv: List[List[float]]
