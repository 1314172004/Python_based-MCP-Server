# app/ccxt_client.py
import asyncio
import ccxt.async_support as ccxt_async
from typing import Optional, List
import time

async def get_exchange(exchange_id: str):
    exchange_cls = getattr(ccxt_async, exchange_id, None)
    if exchange_cls is None:
        raise ValueError(f"Exchange '{exchange_id}' not supported by ccxt")
    return exchange_cls()

async def fetch_ticker(exchange_id: str, symbol: str) -> dict:
    exch = await get_exchange(exchange_id)
    try:
        await exch.load_markets()
        ticker = await exch.fetch_ticker(symbol)
        return ticker
    finally:
        await exch.close()

async def fetch_ohlcv(exchange_id: str, symbol: str, timeframe: str='1m', since: Optional[int]=None, limit: int=100) -> List:
    exch = await get_exchange(exchange_id)
    try:
        await exch.load_markets()
        ohlcv = await exch.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        return ohlcv
    finally:
        await exch.close()
