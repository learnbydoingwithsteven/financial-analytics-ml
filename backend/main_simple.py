"""
Simplified FastAPI Backend for Testing
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import logging

from config import ASSETS, CORS_ORIGINS
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Financial Analytics API - Test Version",
    description="Testing basic functionality",
    version="1.0.0-test"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_fetcher = DataFetcher()
technical_indicators = TechnicalIndicators()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Financial Analytics API - Test Version",
        "version": "1.0.0-test",
        "status": "running"
    }

@app.get("/api/assets")
async def get_assets():
    """Get list of all tracked assets"""
    return {
        "assets": [
            {
                "symbol": asset.symbol,
                "name": asset.name,
                "category": asset.category,
                "exchange": asset.exchange
            }
            for asset in ASSETS.values()
        ]
    }

@app.get("/api/data/{symbol}")
async def get_data(symbol: str, period: str = "1y"):
    """Get historical data for a symbol"""
    if symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
    
    df = data_fetcher.get_historical_data(symbol, period=period)
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {symbol}")
    
    # Convert to dict for JSON response
    data = df.to_dict(orient='records')
    
    return {
        "symbol": symbol,
        "name": ASSETS[symbol].name,
        "period": period,
        "records": len(data),
        "data": data[:100]  # Limit to first 100 records for testing
    }

@app.get("/api/indicators/{symbol}")
async def get_indicators(symbol: str, period: str = "1y"):
    """Get technical indicators for a symbol"""
    if symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
    
    df = data_fetcher.get_historical_data(symbol, period=period)
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {symbol}")
    
    try:
        df_indicators = technical_indicators.calculate_all_indicators(df)
        latest = df_indicators.iloc[-1]
        
        import pandas as pd
        
        return {
            "symbol": symbol,
            "name": ASSETS[symbol].name,
            "latest_price": float(latest['close']),
            "indicators": {
                "moving_averages": {
                    "sma_20": float(latest['sma_20']) if pd.notna(latest['sma_20']) else None,
                    "sma_50": float(latest['sma_50']) if pd.notna(latest['sma_50']) else None,
                },
                "momentum": {
                    "rsi": float(latest['rsi']) if pd.notna(latest['rsi']) else None,
                },
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/signals/{symbol}")
async def get_signals(symbol: str, period: str = "1y"):
    """Get buy/sell signals for a symbol"""
    if symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
    
    df = data_fetcher.get_historical_data(symbol, period=period)
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {symbol}")
    
    try:
        df_indicators = technical_indicators.calculate_all_indicators(df)
        signals = technical_indicators.generate_signals(df_indicators)
        
        return {
            "symbol": symbol,
            "name": ASSETS[symbol].name,
            "signals": signals
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=False)
