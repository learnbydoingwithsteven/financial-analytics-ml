"""
Configuration settings for the financial analytics backend
"""
from typing import Dict, List
from pydantic import BaseModel

class AssetConfig(BaseModel):
    """Asset configuration"""
    symbol: str
    name: str
    category: str
    exchange: str = ""

# Asset definitions
ASSETS: Dict[str, AssetConfig] = {
    # Forex
    "EURCNY=X": AssetConfig(symbol="EURCNY=X", name="EUR/CNY", category="forex", exchange="FX"),
    
    # Commodities
    "GC=F": AssetConfig(symbol="GC=F", name="Gold Futures", category="commodity", exchange="COMEX"),
    
    # US Bonds
    "TLT": AssetConfig(symbol="TLT", name="US 20+ Year Treasury Bond ETF", category="us_bond", exchange="NYSE"),
    "IEF": AssetConfig(symbol="IEF", name="US 7-10 Year Treasury Bond ETF", category="us_bond", exchange="NYSE"),
    
    # China Bonds (using ETFs as proxy)
    "CBON": AssetConfig(symbol="CBON", name="VanEck China Bond ETF", category="cn_bond", exchange="NYSE"),
    
    # US Indexes
    "^GSPC": AssetConfig(symbol="^GSPC", name="S&P 500", category="us_index", exchange="US"),
    "^DJI": AssetConfig(symbol="^DJI", name="Dow Jones Industrial Average", category="us_index", exchange="US"),
    "^IXIC": AssetConfig(symbol="^IXIC", name="NASDAQ Composite", category="us_index", exchange="US"),
    
    # China Indexes
    "000001.SS": AssetConfig(symbol="000001.SS", name="Shanghai Composite", category="cn_index", exchange="SSE"),
    "399001.SZ": AssetConfig(symbol="399001.SZ", name="Shenzhen Component", category="cn_index", exchange="SZSE"),
    "^HSI": AssetConfig(symbol="^HSI", name="Hang Seng Index", category="cn_index", exchange="HKEX"),
}

# Technical Indicator Parameters
INDICATOR_PARAMS = {
    "sma_periods": [20, 50, 200],
    "ema_periods": [12, 26],
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bb_period": 20,
    "bb_std": 2,
    "stoch_period": 14,
    "cci_period": 20,
    "atr_period": 14,
}

# ML Model Configuration
ML_MODELS = [
    "lstm",
    "random_forest",
    "xgboost",
    "prophet",
    "arima",
    "ensemble"
]

# Prediction time horizons (in trading days)
PREDICTION_HORIZONS = {
    "1m": 21,   # ~1 month
    "2m": 42,   # ~2 months
    "3m": 63,   # ~3 months
    "6m": 126,  # ~6 months
}

# Data settings
DATA_LOOKBACK_DAYS = 730  # 2 years of historical data
UPDATE_INTERVAL_MINUTES = 60  # Update data every hour

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8001
API_RELOAD = True

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
