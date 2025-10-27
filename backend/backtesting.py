"""
Advanced Backtesting and Prediction System
Supports historical testing and future predictions with multiple configurations
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class BacktestingEngine:
    """Engine for running backtests with different configurations"""
    
    def __init__(self, ml_predictor):
        self.ml_predictor = ml_predictor
        
    def prepare_historical_backtest(
        self,
        df: pd.DataFrame,
        test_period: str,  # 'current_month' or 'current_3months'
        train_lookback: str,  # '1month', '2months', '3months', '6months'
        train_test_split: str  # '80_20' or '70_30'
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Prepare data for historical backtesting
        
        Args:
            df: Full historical dataframe
            test_period: How much recent data to use as test (to simulate prediction)
            train_lookback: How much historical data to use for training
            train_test_split: Ratio for train/test split
            
        Returns:
            train_df, val_df, test_df
        """
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Determine test period (most recent data)
        if test_period == 'current_month':
            test_days = 30
        elif test_period == 'current_3months':
            test_days = 90
        else:
            test_days = 30
            
        # Get test data (most recent)
        test_df = df.iloc[-test_days:]
        
        # Determine train lookback period
        lookback_days = {
            '1month': 30,
            '2months': 60,
            '3months': 90,
            '6months': 180,
            '1year': 365
        }
        train_length = lookback_days.get(train_lookback, 60)
        
        # Get training data (before test period)
        available_train = df.iloc[:-test_days]
        train_data = available_train.iloc[-train_length:]
        
        # Split training data into train and validation
        split_ratio = float(train_test_split.split('_')[0]) / 100
        split_idx = int(len(train_data) * split_ratio)
        
        train_df = train_data.iloc[:split_idx]
        val_df = train_data.iloc[split_idx:]
        
        logger.info(f"Backtest setup - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
        
        return train_df, val_df, test_df
    
    def run_backtest(
        self,
        df: pd.DataFrame,
        config: Dict
    ) -> Dict:
        """
        Run a single backtest configuration
        
        Args:
            df: Full historical data
            config: Configuration dict with test_period, train_lookback, train_test_split
            
        Returns:
            Results including predictions and metrics
        """
        test_period = config.get('test_period', 'current_month')
        train_lookback = config.get('train_lookback', '2months')
        train_test_split = config.get('train_test_split', '80_20')
        
        # Prepare data
        train_df, val_df, test_df = self.prepare_historical_backtest(
            df, test_period, train_lookback, train_test_split
        )
        
        # Combine train and val for model training
        full_train_df = pd.concat([train_df, val_df], ignore_index=True)
        
        # Train models
        logger.info(f"Training models with config: {config}")
        training_results = self.ml_predictor.train_all_models(full_train_df)
        
        # Generate predictions for test period (day by day)
        predictions = {}
        test_dates = test_df['date'].tolist()
        
        for model_name in self.ml_predictor.models.keys():
            try:
                # Predict using trained model
                pred_result = self.ml_predictor.predict_single_model(
                    model_name,
                    full_train_df,
                    horizon=len(test_df)
                )
                
                if pred_result.get('success', False):
                    predictions[model_name] = {
                        'dates': [d.strftime('%Y-%m-%d') for d in test_dates],
                        'predictions': pred_result['predictions'][:len(test_dates)],
                        'actual': test_df['close'].tolist(),
                        'lower_bound': pred_result.get('lower_bound', [])[:len(test_dates)],
                        'upper_bound': pred_result.get('upper_bound', [])[:len(test_dates)]
                    }
            except Exception as e:
                logger.error(f"Error predicting with {model_name}: {e}")
        
        # Calculate ensemble prediction
        try:
            ensemble_result = self.ml_predictor.predict_ensemble(full_train_df, len(test_df))
            if ensemble_result.get('success', False):
                predictions['ensemble'] = {
                    'dates': [d.strftime('%Y-%m-%d') for d in test_dates],
                    'predictions': ensemble_result['predictions'][:len(test_dates)],
                    'actual': test_df['close'].tolist(),
                    'lower_bound': ensemble_result.get('lower_bound', [])[:len(test_dates)],
                    'upper_bound': ensemble_result.get('upper_bound', [])[:len(test_dates)]
                }
        except Exception as e:
            logger.error(f"Error in ensemble prediction: {e}")
        
        # Calculate accuracy metrics for each model
        accuracy_metrics = {}
        for model_name, pred_data in predictions.items():
            actual = np.array(pred_data['actual'])
            predicted = np.array(pred_data['predictions'])
            
            # Calculate metrics
            mse = np.mean((actual - predicted) ** 2)
            rmse = np.sqrt(mse)
            mae = np.mean(np.abs(actual - predicted))
            mape = np.mean(np.abs((actual - predicted) / actual)) * 100
            
            # Direction accuracy
            actual_direction = np.diff(actual) > 0
            pred_direction = np.diff(predicted) > 0
            direction_acc = np.mean(actual_direction == pred_direction) * 100
            
            accuracy_metrics[model_name] = {
                'rmse': float(rmse),
                'mae': float(mae),
                'mape': float(mape),
                'direction_accuracy': float(direction_acc),
                'total_points': len(actual)
            }
        
        return {
            'config': config,
            'training_results': training_results,
            'predictions': predictions,
            'accuracy_metrics': accuracy_metrics,
            'data_info': {
                'train_start': train_df['date'].iloc[0].strftime('%Y-%m-%d'),
                'train_end': val_df['date'].iloc[-1].strftime('%Y-%m-%d'),
                'test_start': test_df['date'].iloc[0].strftime('%Y-%m-%d'),
                'test_end': test_df['date'].iloc[-1].strftime('%Y-%m-%d'),
                'train_samples': len(train_df),
                'val_samples': len(val_df),
                'test_samples': len(test_df)
            }
        }
    
    def compare_configurations(
        self,
        df: pd.DataFrame,
        configs: List[Dict]
    ) -> Dict:
        """
        Run multiple backtest configurations and compare results
        
        Args:
            df: Full historical data
            configs: List of configuration dictionaries
            
        Returns:
            Comparison results with best configuration
        """
        results = []
        
        for config in configs:
            logger.info(f"Running backtest: {config}")
            result = self.run_backtest(df, config)
            results.append(result)
        
        # Find best configuration for each model
        best_configs = {}
        for model_name in results[0]['predictions'].keys():
            best_config = min(
                results,
                key=lambda r: r['accuracy_metrics'][model_name]['rmse']
            )
            best_configs[model_name] = {
                'config': best_config['config'],
                'metrics': best_config['accuracy_metrics'][model_name]
            }
        
        # Retrain models with the best configuration for ensemble
        # This ensures ml_predictor.training_results is populated for ModelPerformance component
        if best_configs and 'ensemble' in best_configs:
            best_ensemble_config = best_configs['ensemble']['config']
            logger.info(f"Retraining models with best ensemble configuration for performance display")
            
            train_df, val_df, test_df = self.prepare_historical_backtest(
                df,
                best_ensemble_config['test_period'],
                best_ensemble_config['train_lookback'],
                best_ensemble_config['train_test_split']
            )
            full_train_df = pd.concat([train_df, val_df], ignore_index=True)
            self.ml_predictor.train_all_models(full_train_df)
        
        return {
            'all_results': results,
            'best_configs': best_configs,
            'comparison_summary': self._create_comparison_summary(results)
        }
    
    def _create_comparison_summary(self, results: List[Dict]) -> List[Dict]:
        """Create a summary table comparing all configurations"""
        summary = []
        
        for result in results:
            config = result['config']
            config_str = f"{config['test_period']}_train{config['train_lookback']}_split{config['train_test_split']}"
            
            for model_name, metrics in result['accuracy_metrics'].items():
                summary.append({
                    'configuration': config_str,
                    'model': model_name,
                    **metrics
                })
        
        return summary
    
    def predict_future(
        self,
        df: pd.DataFrame,
        best_config: Dict,
        prediction_horizon: str  # '1month' or '3months'
    ) -> Dict:
        """
        Use best configuration to predict future prices
        
        Args:
            df: Full historical data (used for training)
            best_config: Best configuration from backtesting
            prediction_horizon: How far into future to predict
            
        Returns:
            Future predictions for all models
        """
        horizon_days = {
            '1month': 30,
            '3months': 90
        }
        days_ahead = horizon_days.get(prediction_horizon, 30)
        
        # Train on full recent data
        train_lookback = best_config.get('train_lookback', '2months')
        lookback_days = {
            '1month': 30,
            '2months': 60,
            '3months': 90,
            '6months': 180
        }
        train_length = lookback_days.get(train_lookback, 60)
        train_df = df.iloc[-train_length:]
        
        # Train models
        logger.info(f"Training models on recent {train_length} days for future prediction")
        self.ml_predictor.train_all_models(train_df)
        
        # Generate future predictions
        last_date = pd.to_datetime(df['date'].iloc[-1])
        future_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=days_ahead,
            freq='D'
        )
        
        future_predictions = {}
        for model_name in self.ml_predictor.models.keys():
            try:
                pred_result = self.ml_predictor.predict_single_model(
                    model_name,
                    train_df,
                    horizon=days_ahead
                )
                
                if pred_result.get('success', False):
                    future_predictions[model_name] = {
                        'dates': [d.strftime('%Y-%m-%d') for d in future_dates],
                        'predictions': pred_result['predictions'],
                        'lower_bound': pred_result.get('lower_bound', []),
                        'upper_bound': pred_result.get('upper_bound', [])
                    }
            except Exception as e:
                logger.error(f"Error predicting future with {model_name}: {e}")
        
        # Ensemble prediction
        try:
            ensemble_result = self.ml_predictor.predict_ensemble(train_df, days_ahead)
            if ensemble_result.get('success', False):
                future_predictions['ensemble'] = {
                    'dates': [d.strftime('%Y-%m-%d') for d in future_dates],
                    'predictions': ensemble_result['predictions'],
                    'lower_bound': ensemble_result.get('lower_bound', []),
                    'upper_bound': ensemble_result.get('upper_bound', [])
                }
        except Exception as e:
            logger.error(f"Error in ensemble future prediction: {e}")
        
        return {
            'prediction_horizon': prediction_horizon,
            'days_ahead': days_ahead,
            'start_date': future_dates[0].strftime('%Y-%m-%d'),
            'end_date': future_dates[-1].strftime('%Y-%m-%d'),
            'last_historical_date': last_date.strftime('%Y-%m-%d'),
            'last_historical_price': float(df['close'].iloc[-1]),
            'predictions': future_predictions
        }
