import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getPredictions, trainModels } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, ComposedChart } from 'recharts';
import { Loader2, Brain, TrendingUp, TrendingDown, Play, CheckCircle, AlertCircle } from 'lucide-react';

const MLPredictions = ({ symbol, period = '2y' }) => {
  const [selectedHorizon, setSelectedHorizon] = useState('1m');
  const [selectedModel, setSelectedModel] = useState('ensemble');
  const [trainingStatus, setTrainingStatus] = useState(null);
  const [showDateRangeOptions, setShowDateRangeOptions] = useState(false);
  const [trainStartDate, setTrainStartDate] = useState('');
  const [trainEndDate, setTrainEndDate] = useState('');
  const [testStartDate, setTestStartDate] = useState('');
  const [testEndDate, setTestEndDate] = useState('');
  const queryClient = useQueryClient();

  // Query for predictions (only enabled if not training)
  const { data, isLoading, error } = useQuery({
    queryKey: ['predictions', symbol],
    queryFn: () => getPredictions(symbol),
    enabled: trainingStatus !== 'training',
    retry: false,
  });

  // Mutation for training models
  const trainMutation = useMutation({
    mutationFn: () => {
      const params = { symbol, period };
      if (trainStartDate) params.train_start_date = trainStartDate;
      if (trainEndDate) params.train_end_date = trainEndDate;
      if (testStartDate) params.test_start_date = testStartDate;
      if (testEndDate) params.test_end_date = testEndDate;
      return trainModels(params.symbol, params.period, params);
    },
    onMutate: () => {
      setTrainingStatus('training');
    },
    onSuccess: () => {
      setTrainingStatus('success');
      // Invalidate and refetch predictions
      queryClient.invalidateQueries({ queryKey: ['predictions', symbol] });
      setTimeout(() => setTrainingStatus(null), 3000);
    },
    onError: (error) => {
      setTrainingStatus('error');
      console.error('Training failed:', error);
      setTimeout(() => setTrainingStatus(null), 5000);
    },
  });

  const handleTrainAndPredict = () => {
    trainMutation.mutate();
  };

  if (isLoading) {
    return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center space-x-2">
            <Brain className="h-5 w-5 text-primary-600" />
            <span>ML Price Predictions</span>
          </div>
        </div>
        <div className="flex flex-col items-center justify-center py-12">
          <Loader2 className="h-12 w-12 animate-spin text-primary-600 mb-4" />
          <p className="text-sm text-gray-600">Training ML models and generating predictions...</p>
          <p className="text-xs text-gray-500 mt-2">This may take 30-60 seconds</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center space-x-2">
            <Brain className="h-5 w-5 text-primary-600" />
            <span>ML Price Predictions</span>
          </div>
        </div>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-yellow-600 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-yellow-900 mb-2">Predictions Not Available Yet</h3>
            <p className="text-sm text-yellow-700 mb-4">
              {error.message.includes('timeout') 
                ? 'The prediction request timed out. This usually means the models need to be trained first.'
                : 'Unable to load predictions at this time.'}
            </p>
            <div className="bg-white rounded-lg p-4 mb-4">
              <p className="text-sm text-gray-700 mb-3">
                <strong>To generate predictions:</strong>
              </p>
              <ol className="text-sm text-left text-gray-600 space-y-2 max-w-md mx-auto">
                <li>1. Click the <strong className="text-blue-600">"Train Models & Generate Predictions"</strong> button above</li>
                <li>2. Wait 30-60 seconds for all 6 models to train</li>
                <li>3. Predictions will appear automatically after training</li>
              </ol>
            </div>
            <button
              onClick={() => handleTrainAndPredict()}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Train Models Now
            </button>
          </div>
        </div>
      </div>
    );
  }

  const predictions = data?.predictions || {};
  const horizonData = predictions[selectedHorizon] || {};
  const modelData = horizonData[selectedModel] || {};

  // Prepare chart data
  const chartData = modelData.predictions?.map((pred, idx) => ({
    day: idx + 1,
    prediction: pred,
    lower: modelData.lower_bound?.[idx],
    upper: modelData.upper_bound?.[idx],
  })) || [];

  // Calculate prediction summary
  const currentPrice = modelData.predictions?.[0];
  const finalPrice = modelData.predictions?.[modelData.predictions?.length - 1];
  const priceDiff = finalPrice - currentPrice;
  const priceDiffPercent = ((priceDiff / currentPrice) * 100).toFixed(2);
  const isUptrend = priceDiff > 0;

  const horizonLabels = {
    '1m': '1 Month',
    '2m': '2 Months',
    '3m': '3 Months',
    '6m': '6 Months',
  };

  const modelLabels = {
    'ensemble': '🎯 Ensemble (Combined)',
    'lstm': '🧠 LSTM Neural Network',
    'random_forest': '🌲 Random Forest',
    'xgboost': '⚡ XGBoost',
    'prophet': '📈 Prophet',
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center space-x-2">
          <Brain className="h-5 w-5 text-primary-600" />
          <span>ML Price Predictions</span>
        </div>
        {modelData.predictions && (
          <div className="text-right">
            <div className={`text-2xl font-bold ${isUptrend ? 'text-green-600' : 'text-red-600'}`}>
              {isUptrend ? <TrendingUp className="inline h-6 w-6" /> : <TrendingDown className="inline h-6 w-6" />}
              {isUptrend ? '+' : ''}{priceDiffPercent}%
            </div>
            <p className="text-sm text-gray-600">Predicted Change</p>
          </div>
        )}
      </div>

      {/* Date Range Options */}
      <div className="mb-4">
        <button
          onClick={() => setShowDateRangeOptions(!showDateRangeOptions)}
          className="text-sm text-blue-600 hover:text-blue-700 flex items-center space-x-1"
        >
          <span>{showDateRangeOptions ? '▼' : '▶'} Advanced: Custom Train/Test Date Range</span>
        </button>
        
        {showDateRangeOptions && (
          <div className="mt-3 p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <p className="text-xs text-gray-600 mb-3">
              <strong>Time Series Split:</strong> For time series data, train on earlier dates and test on later dates.
              Leave empty to use automatic 80/20 split.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Training Period</label>
                <div className="space-y-2">
                  <input
                    type="date"
                    value={trainStartDate}
                    onChange={(e) => setTrainStartDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                    placeholder="Start Date"
                  />
                  <input
                    type="date"
                    value={trainEndDate}
                    onChange={(e) => setTrainEndDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                    placeholder="End Date"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Test Period (Future dates)</label>
                <div className="space-y-2">
                  <input
                    type="date"
                    value={testStartDate}
                    onChange={(e) => setTestStartDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                    placeholder="Start Date"
                  />
                  <input
                    type="date"
                    value={testEndDate}
                    onChange={(e) => setTestEndDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                    placeholder="End Date"
                  />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Train Button */}
      <div className="mb-6">
        <button
          onClick={handleTrainAndPredict}
          disabled={trainingStatus === 'training'}
          className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {trainingStatus === 'training' ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Training Models... (30-60s)</span>
            </>
          ) : trainingStatus === 'success' ? (
            <>
              <CheckCircle className="h-5 w-5" />
              <span>Training Complete!</span>
            </>
          ) : trainingStatus === 'error' ? (
            <>
              <AlertCircle className="h-5 w-5" />
              <span>Training Failed - Try Again</span>
            </>
          ) : (
            <>
              <Play className="h-5 w-5" />
              <span>Train Models & Generate Predictions</span>
            </>
          )}
        </button>
        {trainingStatus === 'training' && (
          <p className="text-sm text-gray-600 mt-2 text-center">
            Training 6 ML models: LSTM, Random Forest, XGBoost, Prophet, ARIMA, and Ensemble
          </p>
        )}
      </div>

      {/* Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Time Horizon
          </label>
          <select
            value={selectedHorizon}
            onChange={(e) => setSelectedHorizon(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500"
          >
            {Object.keys(horizonLabels).map((key) => (
              <option key={key} value={key}>
                {horizonLabels[key]}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ML Model
          </label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500"
          >
            {Object.keys(modelLabels).map((key) => (
              <option key={key} value={key}>
                {modelLabels[key]}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Prediction Chart */}
      {modelData.predictions ? (
        <>
          <ResponsiveContainer width="100%" height={350}>
            <ComposedChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="day" 
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                label={{ value: 'Days Ahead', position: 'insideBottom', offset: -5 }}
              />
              <YAxis 
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                label={{ value: 'Price', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="upper"
                fill="#93c5fd"
                stroke="none"
                fillOpacity={0.3}
                name="Upper Bound"
              />
              <Area
                type="monotone"
                dataKey="lower"
                fill="#93c5fd"
                stroke="none"
                fillOpacity={0.3}
                name="Lower Bound"
              />
              <Line 
                type="monotone" 
                dataKey="prediction" 
                stroke="#0ea5e9" 
                strokeWidth={3}
                dot={{ fill: '#0ea5e9', r: 4 }}
                name="Prediction"
              />
            </ComposedChart>
          </ResponsiveContainer>

          {/* Prediction Summary */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-600 mb-1">Current</p>
              <p className="text-2xl font-bold text-blue-900">
                ${currentPrice?.toFixed(2)}
              </p>
            </div>
            <div className={`${isUptrend ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'} border rounded-lg p-4`}>
              <p className={`text-sm ${isUptrend ? 'text-green-600' : 'text-red-600'} mb-1`}>
                Predicted ({horizonLabels[selectedHorizon]})
              </p>
              <p className={`text-2xl font-bold ${isUptrend ? 'text-green-900' : 'text-red-900'}`}>
                ${finalPrice?.toFixed(2)}
              </p>
            </div>
            <div className={`${isUptrend ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'} border rounded-lg p-4`}>
              <p className={`text-sm ${isUptrend ? 'text-green-600' : 'text-red-600'} mb-1`}>
                Expected Change
              </p>
              <p className={`text-2xl font-bold ${isUptrend ? 'text-green-900' : 'text-red-900'}`}>
                {isUptrend ? '+' : ''}{priceDiff?.toFixed(2)} ({isUptrend ? '+' : ''}{priceDiffPercent}%)
              </p>
            </div>
          </div>
        </>
      ) : (
        <div className="text-center py-12 text-gray-500">
          No predictions available for this configuration
        </div>
      )}
    </div>
  );
};

export default MLPredictions;
