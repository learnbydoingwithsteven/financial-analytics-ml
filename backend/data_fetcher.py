"""
Data fetching module using free Yahoo Finance API
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    """Fetch financial data from Yahoo Finance"""
    
    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}
        self.cache_timestamp: Dict[str, datetime] = {}
        self.cache_duration = timedelta(minutes=60)
    
    def get_historical_data(
        self,
        symbol: str,
        period: str = "2y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical data for a symbol
        
        Args:
            symbol: Ticker symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            DataFrame with OHLCV data
        """
        cache_key = f"{symbol}_{period}_{interval}"
        
        # Check cache
        if cache_key in self.cache:
            if datetime.now() - self.cache_timestamp[cache_key] < self.cache_duration:
                logger.info(f"Returning cached data for {symbol}")
                return self.cache[cache_key]
        
        try:
            logger.info(f"Fetching data for {symbol}")
            
            # Convert period to explicit start/end dates to avoid yfinance datetime bugs
            end_date = datetime.now()
            period_map = {
                '1d': 1, '5d': 5, '1mo': 30, '3mo': 90, '6mo': 180,
                '1y': 365, '2y': 730, '5y': 1825, '10y': 3650, 'max': 7300
            }
            days = period_map.get(period, 730)  # Default to 2 years
            start_date = end_date - timedelta(days=days)
            
            ticker = yf.Ticker(symbol)
            # Use explicit start and end dates instead of period
            df = ticker.history(start=start_date.strftime('%Y-%m-%d'), 
                              end=end_date.strftime('%Y-%m-%d'), 
                              interval=interval)
            
            if df.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            # Clean data
            df = df.reset_index()
            df.columns = [col.lower() if col != 'Date' else 'date' for col in df.columns]
            
            # Cache the data
            self.cache[cache_key] = df
            self.cache_timestamp[cache_key] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """Get latest price for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            logger.error(f"Error fetching latest price for {symbol}: {str(e)}")
            return None
    
    def get_info(self, symbol: str) -> Dict:
        """Get ticker information"""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {str(e)}")
            return {}
    
    def get_multiple_symbols(self, symbols: list, period: str = "2y") -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple symbols"""
        results = {}
        for symbol in symbols:
            df = self.get_historical_data(symbol, period=period)
            if df is not None:
                results[symbol] = df
        return results
    
    def clear_cache(self):
        """Clear the data cache"""
        self.cache = {}
        self.cache_timestamp = {}
        logger.info("Cache cleared")
