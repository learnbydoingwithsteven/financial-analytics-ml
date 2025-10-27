"""
FastAPI Backend for Financial Analytics Dashboard
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging
import pandas as pd

from config import ASSETS, CORS_ORIGINS, PREDICTION_HORIZONS, API_HOST, API_PORT
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from ml_predictor import MLPredictor
from backtesting import BacktestingEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Financial Analytics API",
    description="API for financial data, technical indicators, and ML predictions",
    version="1.0.0"
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
ml_predictor = MLPredictor()
backtesting_engine = BacktestingEngine(ml_predictor)

# Store trained models per symbol
trained_models: Dict[str, bool] = {}

# Pydantic models for request/response
class TrainRequest(BaseModel):
    symbol: str
    period: str = "2y"
    train_start_date: Optional[str] = None  # Format: YYYY-MM-DD
    train_end_date: Optional[str] = None    # Format: YYYY-MM-DD
    test_start_date: Optional[str] = None   # Format: YYYY-MM-DD
    test_end_date: Optional[str] = None     # Format: YYYY-MM-DD

class PredictRequest(BaseModel):
    symbol: str
    model: str = "ensemble"
    horizon: str = "1m"

class BacktestConfig(BaseModel):
    test_period: str  # 'current_month' or 'current_3months'
    train_lookback: str  # '1month', '2months', '3months', '6months'
    train_test_split: str  # '80_20' or '70_30'

class BacktestRequest(BaseModel):
    symbol: str
    period: str = "2y"
    configs: List[BacktestConfig]

class FuturePredictRequest(BaseModel):
    symbol: str
    period: str = "2y"
    best_config: Dict
    prediction_horizon: str  # '1month' or '3months'

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Financial Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "assets": "/api/assets",
            "data": "/api/data/{symbol}",
            "indicators": "/api/indicators/{symbol}",
            "signals": "/api/signals/{symbol}",
            "train": "/api/train",
            "predictions": "/api/predictions/{symbol}",
            "model_performance": "/api/models/performance/{symbol}"
        }
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
        "data": data
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
        
        # Get latest values
        latest = df_indicators.iloc[-1]
        
        # Prepare time series data for chart
        chart_data = []
        for _, row in df_indicators.iterrows():
            chart_data.append({
                'date': row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date']),
                'close': float(row['close']) if pd.notna(row['close']) else None,
                'sma_20': float(row['sma_20']) if pd.notna(row['sma_20']) else None,
                'sma_50': float(row['sma_50']) if pd.notna(row['sma_50']) else None,
                'ema_12': float(row['ema_12']) if pd.notna(row['ema_12']) else None,
                'bb_upper': float(row['bb_upper']) if pd.notna(row['bb_upper']) else None,
                'bb_middle': float(row['bb_middle']) if pd.notna(row['bb_middle']) else None,
                'bb_lower': float(row['bb_lower']) if pd.notna(row['bb_lower']) else None,
            })
        
        indicators_data = {
            "symbol": symbol,
            "name": ASSETS[symbol].name,
            "latest_price": float(latest['close']),
            "data": chart_data,
            "indicators": {
                "moving_averages": {
                    "sma_20": float(latest['sma_20']) if pd.notna(latest['sma_20']) else None,
                    "sma_50": float(latest['sma_50']) if pd.notna(latest['sma_50']) else None,
                    "sma_200": float(latest['sma_200']) if pd.notna(latest['sma_200']) else None,
                    "ema_12": float(latest['ema_12']) if pd.notna(latest['ema_12']) else None,
                    "ema_26": float(latest['ema_26']) if pd.notna(latest['ema_26']) else None,
                },
                "momentum": {
                    "rsi": float(latest['rsi']) if pd.notna(latest['rsi']) else None,
                    "macd": float(latest['macd']) if pd.notna(latest['macd']) else None,
                    "macd_signal": float(latest['macd_signal']) if pd.notna(latest['macd_signal']) else None,
                    "stoch_k": float(latest['stoch_k']) if pd.notna(latest['stoch_k']) else None,
                    "stoch_d": float(latest['stoch_d']) if pd.notna(latest['stoch_d']) else None,
                    "cci": float(latest['cci']) if pd.notna(latest['cci']) else None,
                },
                "volatility": {
                    "bb_upper": float(latest['bb_upper']) if pd.notna(latest['bb_upper']) else None,
                    "bb_middle": float(latest['bb_middle']) if pd.notna(latest['bb_middle']) else None,
                    "bb_lower": float(latest['bb_lower']) if pd.notna(latest['bb_lower']) else None,
                    "atr": float(latest['atr']) if pd.notna(latest['atr']) else None,
                },
                "volume": {
                    "obv": float(latest['obv']) if pd.notna(latest['obv']) else None,
                }
            }
        }
        
        return indicators_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating indicators: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Error generating signals: {str(e)}")

@app.post("/api/train")
async def train_models(request: TrainRequest):
    """Train ML models for a symbol"""
    if request.symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {request.symbol} not found")
    
    df = data_fetcher.get_historical_data(request.symbol, period=request.period)
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {request.symbol}")
    
    # Filter data by date range if provided
    if request.train_start_date or request.test_end_date:
        df['date'] = pd.to_datetime(df['date'])
        
        # If custom date ranges provided, filter accordingly
        if request.train_start_date:
            train_start = pd.to_datetime(request.train_start_date)
            df = df[df['date'] >= train_start]
        
        if request.test_end_date:
            test_end = pd.to_datetime(request.test_end_date)
            df = df[df['date'] <= test_end]
        
        logger.info(f"Using custom date range: {len(df)} samples")
    
    try:
        results = ml_predictor.train_all_models(df)
        trained_models[request.symbol] = True
        
        # Add date range info to results
        date_range_info = {
            'actual_start_date': str(df['date'].min().date()) if not df.empty else None,
            'actual_end_date': str(df['date'].max().date()) if not df.empty else None,
            'total_days': len(df)
        }
        
        return {
            "symbol": request.symbol,
            "name": ASSETS[request.symbol].name,
            "training_results": results,
            "date_range": date_range_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training models: {str(e)}")

@app.get("/api/predictions/{symbol}")
async def get_predictions(symbol: str, model: str = "ensemble"):
    """Get ML predictions for all time horizons - requires models to be trained first"""
    if symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
    
    # Check if models are trained
    if symbol not in trained_models or not trained_models[symbol]:
        raise HTTPException(
            status_code=400, 
            detail=f"Models not trained for {symbol}. Please train models first using /api/train endpoint."
        )
    
    df = data_fetcher.get_historical_data(symbol, period="2y")
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {symbol}")
    
    try:
        predictions = ml_predictor.get_all_predictions(df, PREDICTION_HORIZONS)
        
        return {
            "symbol": symbol,
            "name": ASSETS[symbol].name,
            "predictions": predictions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting predictions: {str(e)}")

@app.get("/api/models/performance/{symbol}")
async def get_model_performance(symbol: str):
    """Get model performance comparison"""
    if symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
    
    df = data_fetcher.get_historical_data(symbol, period="2y")
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {symbol}")
    
    try:
        performance = ml_predictor.calculate_model_performance(df)
        
        return {
            "symbol": symbol,
            "name": ASSETS[symbol].name,
            "performance": performance
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating performance: {str(e)}")

@app.get("/api/latest/{symbol}")
async def get_latest_price(symbol: str):
    """Get latest price for a symbol"""
    if symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
    
    price = data_fetcher.get_latest_price(symbol)
    
    if price is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch latest price for {symbol}")
    
    return {
        "symbol": symbol,
        "name": ASSETS[symbol].name,
        "price": price
    }

@app.post("/api/backtest")
async def run_backtest(request: BacktestRequest):
    """Run historical backtest with multiple configurations"""
    if request.symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {request.symbol} not found")
    
    df = data_fetcher.get_historical_data(request.symbol, period=request.period)
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {request.symbol}")
    
    try:
        # Convert configs to dict format
        configs = [config.dict() for config in request.configs]
        
        # Run comparison
        results = backtesting_engine.compare_configurations(df, configs)
        
        # Mark models as trained for this symbol
        trained_models[request.symbol] = True
        
        return {
            "symbol": request.symbol,
            "name": ASSETS[request.symbol].name,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in backtest: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error running backtest: {str(e)}")

@app.post("/api/predict-future")
async def predict_future(request: FuturePredictRequest):
    """Predict future prices using best configuration from backtesting"""
    if request.symbol not in ASSETS:
        raise HTTPException(status_code=404, detail=f"Symbol {request.symbol} not found")
    
    df = data_fetcher.get_historical_data(request.symbol, period=request.period)
    
    if df is None:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data for {request.symbol}")
    
    try:
        # Predict future
        future_predictions = backtesting_engine.predict_future(
            df,
            request.best_config,
            request.prediction_horizon
        )
        
        # Add historical data for continuity in charts
        historical_tail = df.tail(30).to_dict('records')
        for record in historical_tail:
            if 'date' in record:
                record['date'] = record['date'].strftime('%Y-%m-%d') if hasattr(record['date'], 'strftime') else str(record['date'])
        
        return {
            "symbol": request.symbol,
            "name": ASSETS[request.symbol].name,
            "historical_tail": historical_tail,
            "future_predictions": future_predictions
        }
        
    except Exception as e:
        logger.error(f"Error in future prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error predicting future: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
