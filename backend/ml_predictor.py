"""
ML Predictor - Orchestrates all ML models and provides ensemble predictions
"""
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

from ml_models import LSTMModel, RandomForestModel, XGBoostModel, ProphetModel

logger = logging.getLogger(__name__)

class MLPredictor:
    """Orchestrate multiple ML models for predictions"""
    
    def __init__(self):
        self.models = {
            'lstm': LSTMModel(),
            'random_forest': RandomForestModel(),
            'xgboost': XGBoostModel(),
            'prophet': ProphetModel()
        }
        self.model_weights = {
            'lstm': 0.25,
            'random_forest': 0.25,
            'xgboost': 0.30,
            'prophet': 0.20
        }
        self.training_results = {}
    
    def train_all_models(self, df: pd.DataFrame) -> Dict:
        """Train all available models"""
        results = {}
        
        for model_name, model in self.models.items():
            logger.info(f"Training {model_name}...")
            try:
                result = model.train(df)
                results[model_name] = result
                self.training_results[model_name] = result
            except Exception as e:
                logger.error(f"Error training {model_name}: {str(e)}")
                results[model_name] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    def predict_single_model(
        self,
        model_name: str,
        df: pd.DataFrame,
        horizon: int
    ) -> Dict:
        """Get predictions from a single model"""
        if model_name not in self.models:
            return {
                'success': False,
                'error': f'Model {model_name} not found'
            }
        
        try:
            return self.models[model_name].predict(df, horizon)
        except Exception as e:
            logger.error(f"Error predicting with {model_name}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_ensemble(self, df: pd.DataFrame, horizon: int) -> Dict:
        """Get ensemble predictions from all models"""
        all_predictions = {}
        successful_models = []
        
        # Get predictions from each model
        for model_name, model in self.models.items():
            try:
                result = model.predict(df, horizon)
                if result.get('success', False):
                    all_predictions[model_name] = result
                    successful_models.append(model_name)
            except Exception as e:
                logger.error(f"Error getting predictions from {model_name}: {str(e)}")
        
        if not successful_models:
            return {
                'success': False,
                'error': 'No models produced successful predictions'
            }
        
        # Calculate weighted ensemble
        ensemble_predictions = np.zeros(horizon)
        ensemble_lower = np.zeros(horizon)
        ensemble_upper = np.zeros(horizon)
        
        total_weight = sum(self.model_weights[m] for m in successful_models)
        
        for model_name in successful_models:
            weight = self.model_weights[model_name] / total_weight
            predictions = np.array(all_predictions[model_name]['predictions'])
            lower = np.array(all_predictions[model_name]['lower_bound'])
            upper = np.array(all_predictions[model_name]['upper_bound'])
            
            ensemble_predictions += weight * predictions
            ensemble_lower += weight * lower
            ensemble_upper += weight * upper
        
        return {
            'success': True,
            'model': 'ensemble',
            'predictions': [float(p) for p in ensemble_predictions],
            'lower_bound': [float(l) for l in ensemble_lower],
            'upper_bound': [float(u) for u in ensemble_upper],
            'horizon': horizon,
            'models_used': successful_models,
            'individual_predictions': {
                model: all_predictions[model]['predictions']
                for model in successful_models
            }
        }
    
    def get_all_predictions(
        self,
        df: pd.DataFrame,
        horizons: Dict[str, int]
    ) -> Dict:
        """Get predictions for all horizons from all models"""
        results = {}
        
        for horizon_name, horizon_days in horizons.items():
            results[horizon_name] = {}
            
            # Get predictions from each model
            for model_name in self.models.keys():
                results[horizon_name][model_name] = self.predict_single_model(
                    model_name, df, horizon_days
                )
            
            # Get ensemble prediction
            results[horizon_name]['ensemble'] = self.predict_ensemble(
                df, horizon_days
            )
        
        return results
    
    def calculate_model_performance(self, df: pd.DataFrame) -> Dict:
        """Calculate and compare model performance"""
        if not self.training_results:
            return {'error': 'No models trained yet'}
        
        performance = {}
        
        for model_name, result in self.training_results.items():
            if result.get('success', False):
                metrics = result.get('metrics', {})
                performance[model_name] = {
                    'rmse': metrics.get('rmse', 0),
                    'mae': metrics.get('mae', 0),
                    'mape': metrics.get('mape', 0),
                    'direction_accuracy': metrics.get('direction_accuracy', 0),
                    'is_trained': self.models[model_name].is_trained
                }
        
        # Calculate ensemble performance as average of individual models
        if performance:
            ensemble_metrics = {
                'rmse': np.mean([m['rmse'] for m in performance.values()]),
                'mae': np.mean([m['mae'] for m in performance.values()]),
                'mape': np.mean([m['mape'] for m in performance.values()]),
                'direction_accuracy': np.mean([m['direction_accuracy'] for m in performance.values()]),
                'is_trained': all(m['is_trained'] for m in performance.values())
            }
            performance['ensemble'] = ensemble_metrics
        
        # Rank models by RMSE (including ensemble)
        if performance:
            ranked_models = sorted(
                performance.items(),
                key=lambda x: x[1]['rmse']
            )
            
            return {
                'performance': performance,
                'best_model': ranked_models[0][0] if ranked_models else None,
                'ranked_models': [
                    {
                        'model': model,
                        'metrics': metrics,
                        'model_specs': self.training_results.get(model, {}).get('model_specs') if model != 'ensemble' else {
                            'total_samples': 'Combined',
                            'train_samples': 'All models',
                            'test_samples': 'All models',
                            'n_features': 'Varies by model',
                            'train_test_split': '80/20',
                            'hyperparameters': {
                                'weights': self.model_weights
                            },
                            'description': 'Weighted combination of all models'
                        }
                    }
                    for model, metrics in ranked_models
                ]
            }
        
        return {'error': 'No performance data available'}
    
    def update_model_weights(self, weights: Dict[str, float]):
        """Update ensemble model weights"""
        total = sum(weights.values())
        if total > 0:
            self.model_weights = {
                model: weight / total
                for model, weight in weights.items()
            }
