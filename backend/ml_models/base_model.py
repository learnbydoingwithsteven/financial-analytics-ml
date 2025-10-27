"""
Base model class for ML predictions
"""
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from sklearn.preprocessing import MinMaxScaler
import logging

logger = logging.getLogger(__name__)

class BaseMLModel(ABC):
    """Abstract base class for ML models"""
    
    def __init__(self, name: str):
        self.name = name
        self.scaler = MinMaxScaler()
        self.is_trained = False
        self.feature_columns = []
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for training/prediction"""
        df = df.copy()
        
        # Create technical features
        df['returns'] = df['close'].pct_change()
        df['log_volume'] = np.log1p(df['volume'])
        
        # Lag features
        for lag in [1, 5, 10]:
            df[f'close_lag_{lag}'] = df['close'].shift(lag)
            df[f'volume_lag_{lag}'] = df['volume'].shift(lag)
        
        # Rolling statistics
        for window in [5, 10, 20]:
            df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
            df[f'std_{window}'] = df['close'].rolling(window=window).std()
            df[f'volume_ma_{window}'] = df['volume'].rolling(window=window).mean()
        
        # Drop NaN values
        df = df.dropna()
        
        # Define feature columns (excluding target and date)
        self.feature_columns = [col for col in df.columns 
                                if col not in ['date', 'close', 'open', 'high', 'low']]
        
        return df
    
    def create_sequences(
        self, 
        data: np.ndarray, 
        target: np.ndarray,
        lookback: int = 60
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for time series prediction"""
        X, y = [], []
        for i in range(lookback, len(data)):
            X.append(data[i-lookback:i])
            y.append(target[i])
        return np.array(X), np.array(y)
    
    def train_test_split(
        self, 
        df: pd.DataFrame, 
        test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split data into train and test sets"""
        split_idx = int(len(df) * (1 - test_size))
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        return train_df, test_df
    
    def calculate_metrics(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray
    ) -> Dict[str, float]:
        """Calculate prediction metrics"""
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_true - y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        # Direction accuracy
        true_direction = np.sign(np.diff(y_true, prepend=y_true[0]))
        pred_direction = np.sign(np.diff(y_pred, prepend=y_pred[0]))
        direction_accuracy = np.mean(true_direction == pred_direction) * 100
        
        return {
            'rmse': float(rmse),
            'mae': float(mae),
            'mape': float(mape),
            'direction_accuracy': float(direction_accuracy)
        }
    
    @abstractmethod
    def train(self, df: pd.DataFrame) -> Dict:
        """Train the model"""
        pass
    
    @abstractmethod
    def predict(self, df: pd.DataFrame, horizon: int) -> Dict:
        """Make predictions"""
        pass
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        return {
            'name': self.name,
            'is_trained': self.is_trained,
            'features': self.feature_columns
        }
