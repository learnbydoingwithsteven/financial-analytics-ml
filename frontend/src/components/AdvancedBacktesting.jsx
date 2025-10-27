import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { runBacktest, predictFuture } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Loader2, Brain, Play, CheckCircle, AlertCircle, TrendingUp, BarChart3, Target, Calendar } from 'lucide-react';

const AdvancedBacktesting = ({ symbol, period = '2y' }) => {
  const [stage, setStage] = useState('config'); // 'config', 'backtesting', 'results', 'future'
  const [selectedConfigs, setSelectedConfigs] = useState([]);
  const [backtestResults, setBacktestResults] = useState(null);
  const [futureResults, setFutureResults] = useState(null);
  const [futurePredictionHorizon, setFuturePredictionHorizon] = useState('1month');
  const queryClient = useQueryClient();

  // Configuration options
  const testPeriods = [
    { value: 'current_month', label: 'Current Month (30 days)' },
    { value: 'current_3months', label: 'Current 3 Months (90 days)' }
  ];

  const trainLookbacks = [
    { value: '1month', label: '1 Month' },
    { value: '2months', label: '2 Months' },
    { value: '3months', label: '3 Months' },
    { value: '6months', label: '6 Months' }
  ];

  const trainTestSplits = [
    { value: '80_20', label: '80/20 Split' },
    { value: '70_30', label: '70/30 Split' }
  ];

  // Backtest mutation
  const backtestMutation = useMutation({
    mutationFn: () => runBacktest(symbol, period, selectedConfigs),
    onSuccess: (data) => {
      setBacktestResults(data.results);
      setStage('results');
      // Invalidate model performance query to trigger refresh
      queryClient.invalidateQueries({ queryKey: ['model-performance', symbol] });
    }
  });

  // Future prediction mutation
  const futureMutation = useMutation({
    mutationFn: () => {
      const bestConfig = backtestResults.best_configs.ensemble.config;
      return predictFuture(symbol, period, bestConfig, futurePredictionHorizon);
    },
    onSuccess: (data) => {
      setFutureResults(data);
      setStage('future');
    }
  });

  const toggleConfig = (config) => {
    const configStr = JSON.stringify(config);
    const exists = selectedConfigs.some(c => JSON.stringify(c) === configStr);
    
    if (exists) {
      setSelectedConfigs(selectedConfigs.filter(c => JSON.stringify(c) !== configStr));
    } else {
      setSelectedConfigs([...selectedConfigs, config]);
    }
  };

  const isConfigSelected = (config) => {
    const configStr = JSON.stringify(config);
    return selectedConfigs.some(c => JSON.stringify(c) === configStr);
  };

  const handleRunBacktest = () => {
    if (selectedConfigs.length === 0) {
      alert('Please select at least one configuration');
      return;
    }
    setStage('backtesting');
    backtestMutation.mutate();
  };

  const handlePredictFuture = () => {
    futureMutation.mutate();
  };

  // Render configuration selection
  const renderConfigSelection = () => (
    <div className="space-y-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <Brain className="h-6 w-6 text-blue-600 mt-1" />
          <div>
            <h3 className="font-bold text-blue-900 mb-2">Advanced Backtesting & Prediction</h3>
            <p className="text-sm text-blue-700 mb-2">
              <strong>Step 1: Historical Backtesting</strong> - Test different configurations on recent historical data
            </p>
            <ul className="text-xs text-blue-600 space-y-1 ml-4">
              <li>• Select multiple configurations to compare</li>
              <li>• Find which setup gives most accurate predictions</li>
              <li>• See detailed metrics for each model</li>
            </ul>
            <p className="text-sm text-blue-700 mt-3 mb-1">
              <strong>Step 2: Future Predictions</strong> - Use best configuration to predict future prices
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {testPeriods.map(testPeriod => (
          <div key={testPeriod.value} className="border-2 border-gray-300 rounded-lg p-4">
            <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
              <Calendar className="h-4 w-4 mr-2" />
              {testPeriod.label}
            </h4>
            <p className="text-xs text-gray-600 mb-3">Test Period (Recent Data)</p>
            
            {trainLookbacks.map(trainLookback => (
              <div key={trainLookback.value} className="mb-3">
                <p className="text-xs font-medium text-gray-700 mb-2">{trainLookback.label} Training</p>
                {trainTestSplits.map(split => {
                  const config = {
                    test_period: testPeriod.value,
                    train_lookback: trainLookback.value,
                    train_test_split: split.value
                  };
                  const selected = isConfigSelected(config);
                  
                  return (
                    <button
                      key={split.value}
                      onClick={() => toggleConfig(config)}
                      className={`w-full text-left text-xs px-3 py-2 rounded mb-1 transition-colors ${
                        selected
                          ? 'bg-green-500 text-white font-semibold'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {selected ? '✓ ' : ''}{split.label}
                    </button>
                  );
                })}
              </div>
            ))}
          </div>
        ))}
      </div>

      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-sm font-semibold text-gray-800">
          Selected Configurations: {selectedConfigs.length}
        </p>
        {selectedConfigs.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {selectedConfigs.map((config, idx) => (
              <span key={idx} className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                {config.test_period.replace('_', ' ')} | Train: {config.train_lookback} | {config.train_test_split.replace('_', '/')}
              </span>
            ))}
          </div>
        )}
      </div>

      <button
        onClick={handleRunBacktest}
        disabled={selectedConfigs.length === 0 || backtestMutation.isPending}
        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        {backtestMutation.isPending ? (
          <>
            <Loader2 className="h-5 w-5 animate-spin" />
            <span>Running Backtests... (30-60s per config)</span>
          </>
        ) : (
          <>
            <Play className="h-5 w-5" />
            <span>Run Historical Backtests ({selectedConfigs.length} configs)</span>
          </>
        )}
      </button>
    </div>
  );

  // Render backtest results
  const renderBacktestResults = () => {
    if (!backtestResults) return null;

    const { all_results, best_configs, comparison_summary } = backtestResults;

    // Find overall best model
    const sortedSummary = [...comparison_summary].sort((a, b) => a.rmse - b.rmse);
    const overallBest = sortedSummary[0];

    // Prepare chart data for a selected result
    const firstResult = all_results[0];
    const chartData = [];
    
    if (firstResult && firstResult.predictions) {
      const models = Object.keys(firstResult.predictions);
      const dates = firstResult.predictions[models[0]].dates;
      
      dates.forEach((date, idx) => {
        const dataPoint = { date };
        models.forEach(model => {
          const predData = firstResult.predictions[model];
          dataPoint[`${model}_pred`] = predData.predictions[idx];
          if (idx === 0) {
            dataPoint.actual = predData.actual[idx];
          } else {
            dataPoint.actual = predData.actual[idx];
          }
        });
        chartData.push(dataPoint);
      });
    }

    return (
      <div className="space-y-6">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <CheckCircle className="h-6 w-6 text-green-600" />
            <h3 className="font-bold text-green-900">Backtesting Complete!</h3>
          </div>
          <p className="text-sm text-green-700">
            Tested {all_results.length} configuration(s) across 5 models. Best overall: <strong>{overallBest.model.toUpperCase()}</strong> with <strong>{overallBest.configuration}</strong>
          </p>
        </div>

        {/* Best Configuration per Model */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4 flex items-center">
            <Target className="h-5 w-5 mr-2 text-blue-600" />
            Best Configuration for Each Model
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {Object.entries(best_configs).map(([model, info]) => (
              <div key={model} className="bg-gray-50 border border-gray-300 rounded p-3">
                <p className="font-semibold text-gray-800 text-sm mb-2">{model.toUpperCase()}</p>
                <div className="text-xs text-gray-600 space-y-1">
                  <p>Test: {info.config.test_period.replace('_', ' ')}</p>
                  <p>Train: {info.config.train_lookback}</p>
                  <p>Split: {info.config.train_test_split.replace('_', '/')}</p>
                  <p className="text-green-600 font-semibold mt-2">RMSE: {info.metrics.rmse.toFixed(4)}</p>
                  <p className="text-blue-600">Dir. Acc: {info.metrics.direction_accuracy.toFixed(1)}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Comparison Table */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4 flex items-center">
            <BarChart3 className="h-5 w-5 mr-2 text-purple-600" />
            Detailed Comparison (Top 10 by RMSE)
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="bg-gray-100">
                  <th className="text-left p-2">Configuration</th>
                  <th className="text-left p-2">Model</th>
                  <th className="text-right p-2">RMSE</th>
                  <th className="text-right p-2">MAE</th>
                  <th className="text-right p-2">MAPE%</th>
                  <th className="text-right p-2">Dir.Acc%</th>
                  <th className="text-right p-2">Points</th>
                </tr>
              </thead>
              <tbody>
                {sortedSummary.slice(0, 10).map((row, idx) => (
                  <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="p-2 text-gray-700">{row.configuration}</td>
                    <td className="p-2 font-semibold">{row.model.toUpperCase()}</td>
                    <td className="p-2 text-right">{row.rmse.toFixed(4)}</td>
                    <td className="p-2 text-right">{row.mae.toFixed(4)}</td>
                    <td className="p-2 text-right">{row.mape.toFixed(2)}%</td>
                    <td className="p-2 text-right text-blue-600">{row.direction_accuracy.toFixed(1)}%</td>
                    <td className="p-2 text-right">{row.total_points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Sample Prediction Chart */}
        {chartData.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <h4 className="font-bold text-gray-900 mb-4">Sample Historical Prediction vs Actual</h4>
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="actual" stroke="#000000" strokeWidth={2} name="Actual" />
                <Line type="monotone" dataKey="ensemble_pred" stroke="#8b5cf6" strokeWidth={2} name="Ensemble" strokeDasharray="5 5" />
                <Line type="monotone" dataKey="xgboost_pred" stroke="#f59e0b" strokeWidth={1.5} name="XGBoost" strokeDasharray="3 3" />
                <Line type="monotone" dataKey="random_forest_pred" stroke="#10b981" strokeWidth={1.5} name="Random Forest" strokeDasharray="3 3" />
                <Line type="monotone" dataKey="lstm_pred" stroke="#ef4444" strokeWidth={1.5} name="LSTM" strokeDasharray="3 3" />
                <Line type="monotone" dataKey="prophet_pred" stroke="#3b82f6" strokeWidth={1.5} name="Prophet" strokeDasharray="3 3" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Future Prediction Button */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-bold text-blue-900 mb-3">Step 2: Predict Future Prices</h4>
          <p className="text-sm text-blue-700 mb-4">
            Use the best configuration to predict future prices beyond historical data
          </p>
          <div className="flex items-center space-x-3 mb-4">
            <label className="text-sm font-medium text-gray-700">Prediction Horizon:</label>
            <select
              value={futurePredictionHorizon}
              onChange={(e) => setFuturePredictionHorizon(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded"
            >
              <option value="1month">Next 1 Month (30 days)</option>
              <option value="3months">Next 3 Months (90 days)</option>
            </select>
          </div>
          <button
            onClick={handlePredictFuture}
            disabled={futureMutation.isPending}
            className="w-full bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 text-white font-semibold py-3 px-6 rounded-lg transition-all flex items-center justify-center space-x-2"
          >
            {futureMutation.isPending ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Generating Future Predictions...</span>
              </>
            ) : (
              <>
                <TrendingUp className="h-5 w-5" />
                <span>Predict Future Prices</span>
              </>
            )}
          </button>
        </div>

        <div className="flex items-center justify-between">
          <button
            onClick={() => { setStage('config'); setBacktestResults(null); setFutureResults(null); }}
            className="text-sm text-blue-600 hover:text-blue-700"
          >
            ← Back to Configuration
          </button>
          {futureResults && (
            <button
              onClick={() => setStage('future')}
              className="text-sm text-green-600 hover:text-green-700 font-medium"
            >
              View Future Predictions →
            </button>
          )}
        </div>
      </div>
    );
  };

  // Render future predictions
  const renderFuturePredictions = () => {
    if (!futureResults) return null;

    const { historical_tail, future_predictions } = futureResults;
    
    // Combine historical and future data for continuous chart
    const chartData = [];
    
    // Add historical data
    historical_tail.forEach(record => {
      chartData.push({
        date: record.date,
        actual: record.close,
        type: 'historical'
      });
    });
    
    // Add future predictions
    const models = Object.keys(future_predictions.predictions);
    const dates = future_predictions.predictions[models[0]].dates;
    
    dates.forEach((date, idx) => {
      const dataPoint = { date, type: 'future' };
      models.forEach(model => {
        const predData = future_predictions.predictions[model];
        dataPoint[`${model}_pred`] = predData.predictions[idx];
        dataPoint[`${model}_lower`] = predData.lower_bound?.[idx];
        dataPoint[`${model}_upper`] = predData.upper_bound?.[idx];
      });
      chartData.push(dataPoint);
    });

    return (
      <div className="space-y-6">
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <TrendingUp className="h-6 w-6 text-purple-600" />
            <h3 className="font-bold text-purple-900">Future Predictions Ready!</h3>
          </div>
          <p className="text-sm text-purple-700">
            Predicting {future_predictions.days_ahead} days ahead from {future_predictions.last_historical_date} to {future_predictions.end_date}
          </p>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-900 mb-4">Historical Data + Future Predictions</h4>
          <p className="text-xs text-gray-600 mb-4">
            Historical (black) continues into Future predictions (colored dashed lines)
          </p>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tick={{ fontSize: 9 }} angle={-45} textAnchor="end" height={80} />
              <YAxis tick={{ fontSize: 10 }} />
              <Tooltip />
              <Legend />
              <ReferenceLine x={historical_tail[historical_tail.length - 1].date} stroke="red" strokeWidth={2} label="Today" />
              <Line type="monotone" dataKey="actual" stroke="#000000" strokeWidth={2} name="Historical Price" dot={false} />
              <Line type="monotone" dataKey="ensemble_pred" stroke="#8b5cf6" strokeWidth={2.5} name="Ensemble (Future)" strokeDasharray="5 5" dot={false} />
              <Line type="monotone" dataKey="xgboost_pred" stroke="#f59e0b" strokeWidth={2} name="XGBoost (Future)" strokeDasharray="3 3" dot={false} />
              <Line type="monotone" dataKey="random_forest_pred" stroke="#10b981" strokeWidth={2} name="Random Forest (Future)" strokeDasharray="3 3" dot={false} />
              <Line type="monotone" dataKey="lstm_pred" stroke="#ef4444" strokeWidth={2} name="LSTM (Future)" strokeDasharray="3 3" dot={false} />
              <Line type="monotone" dataKey="prophet_pred" stroke="#3b82f6" strokeWidth={2} name="Prophet (Future)" strokeDasharray="3 3" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <button
          onClick={() => setStage('results')}
          className="text-sm text-blue-600 hover:text-blue-700"
        >
          ← Back to Backtest Results
        </button>
      </div>
    );
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center space-x-2">
          <Brain className="h-5 w-5 text-primary-600" />
          <span>Advanced ML Backtesting & Predictions</span>
        </div>
      </div>

      {stage === 'config' && renderConfigSelection()}
      {stage === 'backtesting' && (
        <div className="flex flex-col items-center justify-center py-12">
          <Loader2 className="h-16 w-16 animate-spin text-primary-600 mb-4" />
          <p className="text-lg font-semibold text-gray-800">Running Historical Backtests...</p>
          <p className="text-sm text-gray-600 mt-2">Training {selectedConfigs.length} configuration(s) across 5 models</p>
          <p className="text-xs text-gray-500 mt-1">This may take 30-60 seconds per configuration</p>
        </div>
      )}
      {stage === 'results' && renderBacktestResults()}
      {stage === 'future' && renderFuturePredictions()}

      {backtestMutation.isError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mt-4">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <p className="text-sm text-red-700">Error: {backtestMutation.error?.message || 'Failed to run backtest'}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedBacktesting;
