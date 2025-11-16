# app/main.py
import asyncio
from fastapi import FastAPI, WebSocket, HTTPException
from app.ccxt_client import fetch_ticker, fetch_ohlcv
from app.schemas import TickerResponse, HistoricalResponse
from app.cache import cache_ttl
import uvicorn

app = FastAPI(title="MCP Crypto Server")
@app.get("/")
def root():
    return {"message": "Crypto MCP Server running"}
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ticker/{exchange_id}/{symbol}", response_model=TickerResponse)
@cache_ttl(ttl=5)  # cache for 5 seconds
async def get_ticker(exchange_id: str, symbol: str):
    try:
        ticker = await fetch_ticker(exchange_id, symbol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail="Error fetching ticker")
    # Normalize some fields
    return {
        "symbol": ticker.get("symbol"),
        "datetime": ticker.get("datetime"),
        "bid": ticker.get("bid"),
        "ask": ticker.get("ask"),
        "last": ticker.get("last"),
        "info": ticker.get("info"),
    }

@app.get("/historical/{exchange_id}/{symbol}", response_model=HistoricalResponse)
async def get_historical(exchange_id: str, symbol: str, timeframe: str = "1m", limit: int = 100):
    try:
        ohlcv = await fetch_ohlcv(exchange_id, symbol, timeframe=timeframe, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail="Error fetching historical data")
    return {"ohlcv": ohlcv}

# Simple websocket endpoint that streams ticker data for a requested symbol every n seconds
@app.websocket("/ws/{exchange_id}/{symbol}")
async def websocket_ticker(websocket: WebSocket, exchange_id: str, symbol: str, interval: int = 5):
    await websocket.accept()
    try:
        while True:
            try:
                ticker = await fetch_ticker(exchange_id, symbol)
                await websocket.send_json({
                    "symbol": ticker.get("symbol"),
                    "datetime": ticker.get("datetime"),
                    "last": ticker.get("last")
                })
            except Exception as e:
                await websocket.send_json({"error": "failed to fetch"})
            await asyncio.sleep(interval)
    except Exception:
        await websocket.close()

# run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
