"""
Prophet Time Series Forecasting Model
"""
import numpy as np
import pandas as pd
from typing import Dict
import logging

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logging.warning("Prophet not available")

from .base_model import BaseMLModel

logger = logging.getLogger(__name__)

class ProphetModel(BaseMLModel):
    """Prophet model for time series prediction"""
    
    def __init__(self):
        super().__init__("Prophet")
        self.model = None
        self.changepoint_prior_scale = 0.05
        self.seasonality_prior_scale = 10.0
    
    def train(self, df: pd.DataFrame) -> Dict:
        """Train Prophet model"""
        if not PROPHET_AVAILABLE:
            return {
                'success': False,
                'error': 'Prophet not available'
            }
        
        try:
            logger.info(f"Training {self.name} model...")
            
            # Prepare data for Prophet (requires 'ds' and 'y' columns)
            prophet_df = df[['date', 'close']].copy()
            prophet_df.columns = ['ds', 'y']
            
            # Remove timezone if present (Prophet doesn't support timezones)
            if pd.api.types.is_datetime64_any_dtype(prophet_df['ds']):
                prophet_df['ds'] = pd.to_datetime(prophet_df['ds']).dt.tz_localize(None)
            
            # Add volume as additional regressor
            prophet_df['volume'] = df['volume'].values
            
            # Split data
            split_idx = int(len(prophet_df) * 0.8)
            train_df = prophet_df.iloc[:split_idx]
            test_df = prophet_df.iloc[split_idx:]
            
            # Initialize Prophet with custom parameters
            self.model = Prophet(
                changepoint_prior_scale=self.changepoint_prior_scale,
                seasonality_prior_scale=self.seasonality_prior_scale,
                daily_seasonality=True,
                weekly_seasonality=True,
                yearly_seasonality=True,
                interval_width=0.95
            )
            
            # Add volume as regressor
            self.model.add_regressor('volume')
            
            # Train model
            self.model.fit(train_df, algorithm='Newton')
            
            # Make predictions on test set
            forecast = self.model.predict(test_df)
            
            # Calculate metrics
            y_true = test_df['y'].values
            y_pred = forecast['yhat'].values
            metrics = self.calculate_metrics(y_true, y_pred)
            
            self.is_trained = True
            
            return {
                'success': True,
                'model': self.name,
                'metrics': metrics,
                'changepoints': len(self.model.changepoints),
                'seasonality_components': list(self.model.seasonalities.keys()),
                'model_specs': {
                    'total_samples': len(prophet_df),
                    'train_samples': len(train_df),
                    'test_samples': len(test_df),
                    'n_features': 2,  # ds (date) and volume as regressor
                    'train_test_split': '80/20',
                    'hyperparameters': {
                        'changepoint_prior_scale': self.changepoint_prior_scale,
                        'seasonality_prior_scale': self.seasonality_prior_scale,
                        'interval_width': 0.95,
                        'algorithm': 'Newton'
                    },
                    'feature_list': ['date', 'volume'],
                    'seasonality': {
                        'daily': True,
                        'weekly': True,
                        'yearly': True
                    },
                    'regressors': ['volume'],
                    'changepoints_detected': len(self.model.changepoints)
                }
            }
            
        except Exception as e:
            logger.error(f"Error training {self.name}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict(self, df: pd.DataFrame, horizon: int) -> Dict:
        """Make predictions for future periods"""
        if not self.is_trained or self.model is None:
            return {
                'success': False,
                'error': 'Model not trained'
            }
        
        try:
            # Prepare future dataframe
            last_date = pd.to_datetime(df['date'].iloc[-1])
            
            # Remove timezone if present (Prophet doesn't support timezones)
            if last_date.tzinfo is not None:
                last_date = last_date.tz_localize(None)
            
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=horizon,
                freq='D'
            )
            
            future_df = pd.DataFrame({
                'ds': future_dates
            })
            
            # Ensure ds column has no timezone
            if pd.api.types.is_datetime64_any_dtype(future_df['ds']):
                future_df['ds'] = pd.to_datetime(future_df['ds']).dt.tz_localize(None)
            
            # Add volume regressor (use last known value)
            future_df['volume'] = df['volume'].iloc[-1]
            
            # Make predictions
            forecast = self.model.predict(future_df)
            
            predictions = forecast['yhat'].values
            lower_bound = forecast['yhat_lower'].values
            upper_bound = forecast['yhat_upper'].values
            
            return {
                'success': True,
                'model': self.name,
                'predictions': [float(p) for p in predictions],
                'lower_bound': [float(l) for l in lower_bound],
                'upper_bound': [float(u) for u in upper_bound],
                'horizon': horizon,
                'trend': [float(t) for t in forecast['trend'].values]
            }
            
        except Exception as e:
            logger.error(f"Error predicting with {self.name}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
