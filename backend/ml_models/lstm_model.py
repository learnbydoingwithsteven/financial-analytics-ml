"""
LSTM (Long Short-Term Memory) Neural Network Model
"""
import numpy as np
import pandas as pd
from typing import Dict
import logging

try:
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow not available. LSTM model will not work.")

from .base_model import BaseMLModel

logger = logging.getLogger(__name__)

class LSTMModel(BaseMLModel):
    """LSTM model for time series prediction"""
    
    def __init__(self):
        super().__init__("LSTM")
        self.model = None
        self.lookback = 60
        self.epochs = 50
        self.batch_size = 32
    
    def build_model(self, input_shape: tuple) -> Sequential:
        """Build LSTM model architecture"""
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for LSTM model")
        
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(64, return_sequences=True),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1)
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train(self, df: pd.DataFrame) -> Dict:
        """Train LSTM model"""
        if not TENSORFLOW_AVAILABLE:
            return {
                'success': False,
                'error': 'TensorFlow not available'
            }
        
        try:
            logger.info(f"Training {self.name} model...")
            
            # Prepare features
            df_features = self.prepare_features(df)
            
            # Split data
            train_df, test_df = self.train_test_split(df_features)
            
            # Scale features
            train_features = self.scaler.fit_transform(train_df[self.feature_columns])
            test_features = self.scaler.transform(test_df[self.feature_columns])
            
            # Scale target
            train_target = train_df['close'].values
            test_target = test_df['close'].values
            
            # Create sequences
            X_train, y_train = self.create_sequences(
                train_features, 
                train_target, 
                self.lookback
            )
            X_test, y_test = self.create_sequences(
                test_features, 
                test_target, 
                self.lookback
            )
            
            # Build model
            self.model = self.build_model((X_train.shape[1], X_train.shape[2]))
            
            # Train model
            history = self.model.fit(
                X_train, y_train,
                epochs=self.epochs,
                batch_size=self.batch_size,
                validation_data=(X_test, y_test),
                verbose=0
            )
            
            # Calculate metrics
            y_pred = self.model.predict(X_test, verbose=0).flatten()
            metrics = self.calculate_metrics(y_test, y_pred)
            
            self.is_trained = True
            
            return {
                'success': True,
                'model': self.name,
                'metrics': metrics,
                'training_loss': float(history.history['loss'][-1]),
                'validation_loss': float(history.history['val_loss'][-1]),
                'model_specs': {
                    'total_samples': len(df_features),
                    'train_samples': len(X_train),
                    'test_samples': len(X_test),
                    'n_features': len(self.feature_columns),
                    'train_test_split': '80/20',
                    'hyperparameters': {
                        'lookback': self.lookback,
                        'epochs': self.epochs,
                        'batch_size': self.batch_size,
                        'layers': [128, 64, 32],
                        'dropout': 0.2,
                        'optimizer': 'adam'
                    },
                    'feature_list': self.feature_columns,
                    'architecture': '3-layer LSTM (128-64-32 units)',
                    'sequence_length': self.lookback
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
            # Prepare features
            df_features = self.prepare_features(df)
            
            # Scale features
            features = self.scaler.transform(df_features[self.feature_columns])
            
            # Get last sequence
            last_sequence = features[-self.lookback:]
            
            # Make predictions
            predictions = []
            current_sequence = last_sequence.copy()
            
            for _ in range(horizon):
                # Predict next value
                pred = self.model.predict(
                    current_sequence.reshape(1, self.lookback, -1),
                    verbose=0
                )[0, 0]
                predictions.append(pred)
                
                # Update sequence (simple approach - use predicted price)
                # In practice, you'd update all features
                new_row = current_sequence[-1].copy()
                current_sequence = np.vstack([current_sequence[1:], new_row])
            
            # Calculate prediction intervals (simplified)
            std = np.std(predictions)
            lower_bound = np.array(predictions) - 1.96 * std
            upper_bound = np.array(predictions) + 1.96 * std
            
            return {
                'success': True,
                'model': self.name,
                'predictions': [float(p) for p in predictions],
                'lower_bound': [float(l) for l in lower_bound],
                'upper_bound': [float(u) for u in upper_bound],
                'horizon': horizon
            }
            
        except Exception as e:
            logger.error(f"Error predicting with {self.name}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
