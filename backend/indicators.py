"""
Technical indicators calculation and signal generation
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import pandas_ta as ta
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """Calculate technical indicators and generate buy/sell signals"""
    
    def __init__(self):
        pass
    
    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators"""
        df = df.copy()
        
        # Ensure we have the required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain: {required_cols}")
        
        # Trend Indicators
        df = self._add_moving_averages(df)
        df = self._add_macd(df)
        
        # Momentum Indicators
        df = self._add_rsi(df)
        df = self._add_stochastic(df)
        df = self._add_cci(df)
        
        # Volatility Indicators
        df = self._add_bollinger_bands(df)
        df = self._add_atr(df)
        
        # Volume Indicators
        df = self._add_obv(df)
        
        return df
    
    def _add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add SMA and EMA"""
        df['sma_20'] = ta.sma(df['close'], length=20)
        df['sma_50'] = ta.sma(df['close'], length=50)
        df['sma_200'] = ta.sma(df['close'], length=200)
        df['ema_12'] = ta.ema(df['close'], length=12)
        df['ema_26'] = ta.ema(df['close'], length=26)
        return df
    
    def _add_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add MACD indicator"""
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        if macd is not None and not macd.empty:
            df['macd'] = macd['MACD_12_26_9']
            df['macd_signal'] = macd['MACDs_12_26_9']
            df['macd_hist'] = macd['MACDh_12_26_9']
        return df
    
    def _add_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add RSI indicator"""
        df['rsi'] = ta.rsi(df['close'], length=14)
        return df
    
    def _add_stochastic(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add Stochastic Oscillator"""
        stoch = ta.stoch(df['high'], df['low'], df['close'], k=14, d=3)
        if stoch is not None and not stoch.empty:
            df['stoch_k'] = stoch['STOCHk_14_3_3']
            df['stoch_d'] = stoch['STOCHd_14_3_3']
        return df
    
    def _add_cci(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add Commodity Channel Index"""
        df['cci'] = ta.cci(df['high'], df['low'], df['close'], length=20)
        return df
    
    def _add_bollinger_bands(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add Bollinger Bands"""
        bb = ta.bbands(df['close'], length=20, std=2)
        if bb is not None and not bb.empty:
            df['bb_upper'] = bb['BBU_20_2.0']
            df['bb_middle'] = bb['BBM_20_2.0']
            df['bb_lower'] = bb['BBL_20_2.0']
        return df
    
    def _add_atr(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add Average True Range"""
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        return df
    
    def _add_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add On-Balance Volume"""
        df['obv'] = ta.obv(df['close'], df['volume'])
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Generate buy/sell signals based on technical indicators
        
        Returns:
            Dictionary with indicator signals and overall recommendation
        """
        if df.empty or len(df) < 200:
            return {"error": "Insufficient data for signal generation"}
        
        latest = df.iloc[-1]
        signals = {}
        buy_signals = 0
        sell_signals = 0
        total_signals = 0
        
        # Moving Average Signals
        if pd.notna(latest['sma_20']) and pd.notna(latest['sma_50']):
            if latest['close'] > latest['sma_20'] > latest['sma_50']:
                signals['ma_trend'] = {'signal': 'BUY', 'strength': 'strong', 'reason': 'Price above SMA 20 and 50'}
                buy_signals += 2
            elif latest['close'] < latest['sma_20'] < latest['sma_50']:
                signals['ma_trend'] = {'signal': 'SELL', 'strength': 'strong', 'reason': 'Price below SMA 20 and 50'}
                sell_signals += 2
            else:
                signals['ma_trend'] = {'signal': 'NEUTRAL', 'strength': 'weak', 'reason': 'Mixed moving average signals'}
            total_signals += 2
        
        # MACD Signal
        if pd.notna(latest['macd']) and pd.notna(latest['macd_signal']):
            if latest['macd'] > latest['macd_signal'] and latest['macd_hist'] > 0:
                signals['macd'] = {'signal': 'BUY', 'strength': 'medium', 'reason': 'MACD above signal line'}
                buy_signals += 1
            elif latest['macd'] < latest['macd_signal'] and latest['macd_hist'] < 0:
                signals['macd'] = {'signal': 'SELL', 'strength': 'medium', 'reason': 'MACD below signal line'}
                sell_signals += 1
            else:
                signals['macd'] = {'signal': 'NEUTRAL', 'strength': 'weak', 'reason': 'MACD neutral'}
            total_signals += 1
        
        # RSI Signal
        if pd.notna(latest['rsi']):
            if latest['rsi'] < 30:
                signals['rsi'] = {'signal': 'BUY', 'strength': 'strong', 'reason': f'RSI oversold at {latest["rsi"]:.1f}'}
                buy_signals += 2
            elif latest['rsi'] > 70:
                signals['rsi'] = {'signal': 'SELL', 'strength': 'strong', 'reason': f'RSI overbought at {latest["rsi"]:.1f}'}
                sell_signals += 2
            elif latest['rsi'] < 40:
                signals['rsi'] = {'signal': 'BUY', 'strength': 'weak', 'reason': f'RSI bullish at {latest["rsi"]:.1f}'}
                buy_signals += 0.5
            elif latest['rsi'] > 60:
                signals['rsi'] = {'signal': 'SELL', 'strength': 'weak', 'reason': f'RSI bearish at {latest["rsi"]:.1f}'}
                sell_signals += 0.5
            else:
                signals['rsi'] = {'signal': 'NEUTRAL', 'strength': 'neutral', 'reason': f'RSI neutral at {latest["rsi"]:.1f}'}
            total_signals += 2
        
        # Bollinger Bands Signal
        if pd.notna(latest['bb_lower']) and pd.notna(latest['bb_upper']):
            if latest['close'] < latest['bb_lower']:
                signals['bollinger'] = {'signal': 'BUY', 'strength': 'medium', 'reason': 'Price below lower band'}
                buy_signals += 1
            elif latest['close'] > latest['bb_upper']:
                signals['bollinger'] = {'signal': 'SELL', 'strength': 'medium', 'reason': 'Price above upper band'}
                sell_signals += 1
            else:
                signals['bollinger'] = {'signal': 'NEUTRAL', 'strength': 'neutral', 'reason': 'Price within bands'}
            total_signals += 1
        
        # Stochastic Signal
        if pd.notna(latest['stoch_k']) and pd.notna(latest['stoch_d']):
            if latest['stoch_k'] < 20 and latest['stoch_k'] > latest['stoch_d']:
                signals['stochastic'] = {'signal': 'BUY', 'strength': 'medium', 'reason': 'Stochastic oversold and turning up'}
                buy_signals += 1
            elif latest['stoch_k'] > 80 and latest['stoch_k'] < latest['stoch_d']:
                signals['stochastic'] = {'signal': 'SELL', 'strength': 'medium', 'reason': 'Stochastic overbought and turning down'}
                sell_signals += 1
            else:
                signals['stochastic'] = {'signal': 'NEUTRAL', 'strength': 'weak', 'reason': 'Stochastic neutral'}
            total_signals += 1
        
        # Overall recommendation
        if total_signals > 0:
            buy_percentage = (buy_signals / total_signals) * 100
            sell_percentage = (sell_signals / total_signals) * 100
            
            if buy_percentage > 60:
                overall = 'STRONG BUY'
            elif buy_percentage > 50:
                overall = 'BUY'
            elif sell_percentage > 60:
                overall = 'STRONG SELL'
            elif sell_percentage > 50:
                overall = 'SELL'
            else:
                overall = 'HOLD'
            
            signals['overall'] = {
                'recommendation': overall,
                'buy_signals': buy_signals,
                'sell_signals': sell_signals,
                'total_signals': total_signals,
                'buy_percentage': round(buy_percentage, 1),
                'sell_percentage': round(sell_percentage, 1),
                'confidence': round(max(buy_percentage, sell_percentage), 1)
            }
        
        return signals
