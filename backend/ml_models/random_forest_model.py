"""
Random Forest Regression Model
"""
import numpy as np
import pandas as pd
from typing import Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import logging

from .base_model import BaseMLModel

logger = logging.getLogger(__name__)

class RandomForestModel(BaseMLModel):
    """Random Forest model for time series prediction"""
    
    def __init__(self):
        super().__init__("Random Forest")
        self.model = None
        self.n_estimators = 100
        self.max_depth = 20
        self.min_samples_split = 5
    
    def train(self, df: pd.DataFrame) -> Dict:
        """Train Random Forest model"""
        try:
            logger.info(f"Training {self.name} model...")
            
            # Prepare features
            df_features = self.prepare_features(df)
            
            # Split data
            train_df, test_df = self.train_test_split(df_features)
            
            # Prepare training data
            X_train = train_df[self.feature_columns].values
            y_train = train_df['close'].values
            
            X_test = test_df[self.feature_columns].values
            y_test = test_df['close'].values
            
            # Initialize model
            self.model = RandomForestRegressor(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                random_state=42,
                n_jobs=-1
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            metrics = self.calculate_metrics(y_test, y_pred)
            
            # Get feature importance
            feature_importance = dict(zip(
                self.feature_columns,
                self.model.feature_importances_
            ))
            top_features = sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            
            self.is_trained = True
            
            return {
                'success': True,
                'model': self.name,
                'metrics': metrics,
                'top_features': [
                    {'feature': feat, 'importance': float(imp)}
                    for feat, imp in top_features
                ],
                'n_trees': self.n_estimators,
                'model_specs': {
                    'total_samples': len(df_features),
                    'train_samples': len(train_df),
                    'test_samples': len(test_df),
                    'n_features': len(self.feature_columns),
                    'train_test_split': '80/20',
                    'hyperparameters': {
                        'n_estimators': self.n_estimators,
                        'max_depth': self.max_depth,
                        'min_samples_split': self.min_samples_split,
                        'random_state': 42
                    },
                    'feature_list': self.feature_columns
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
            # Prepare features from historical data
            df_features = self.prepare_features(df)
            
            if len(df_features) == 0:
                return {
                    'success': False,
                    'error': 'Insufficient data for feature preparation'
                }
            
            # Make rolling predictions
            predictions = []
            current_df = df.copy()  # Keep original data for rolling window
            
            for step in range(horizon):
                # Prepare features for current state
                features_df = self.prepare_features(current_df)
                
                if len(features_df) == 0:
                    break
                
                # Get latest features
                latest_features = features_df[self.feature_columns].iloc[-1:].values
                
                # Predict next value
                pred = self.model.predict(latest_features)[0]
                predictions.append(pred)
                
                # Create new row with prediction for next iteration
                import pandas as pd
                new_row = pd.DataFrame({
                    'date': [pd.Timestamp.now()],
                    'open': [pred],
                    'high': [pred],
                    'low': [pred],
                    'close': [pred],
                    'volume': [current_df['volume'].iloc[-1]]
                })
                current_df = pd.concat([current_df, new_row], ignore_index=True).tail(200)  # Keep last 200 rows
            
            # Calculate prediction intervals using tree predictions
            tree_predictions = np.array([
                tree.predict(df_features[self.feature_columns].iloc[-1:].values)
                for tree in self.model.estimators_
            ])
            std = np.std(tree_predictions) * np.sqrt(np.arange(1, horizon + 1))
            
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
