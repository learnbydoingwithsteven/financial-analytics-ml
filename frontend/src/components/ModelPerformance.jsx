import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getModelPerformance } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { Loader2, Award, Target, Info, ChevronDown, ChevronUp } from 'lucide-react';

const ModelPerformance = ({ symbol }) => {
  const [showSpecs, setShowSpecs] = useState(false);
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['model-performance', symbol],
    queryFn: () => getModelPerformance(symbol),
  });

  if (isLoading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-yellow-50 border border-yellow-200">
        <p className="text-yellow-600">Model performance data not available yet. Train models first.</p>
      </div>
    );
  }

  const performance = data?.performance?.performance || {};
  const bestModel = data?.performance?.best_model;
  const rankedModels = data?.performance?.ranked_models || [];

  // Prepare chart data
  const chartData = rankedModels.map(item => ({
    model: item.model.toUpperCase(),
    rmse: item.metrics.rmse,
    mae: item.metrics.mae,
    accuracy: item.metrics.direction_accuracy,
  }));

  const COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444'];

  const MetricCard = ({ title, value, subtitle, color }) => (
    <div className={`${color} border rounded-lg p-4`}>
      <p className="text-sm opacity-75 mb-1">{title}</p>
      <p className="text-2xl font-bold mb-1">{value}</p>
      <p className="text-xs opacity-60">{subtitle}</p>
    </div>
  );

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center space-x-2">
          <Award className="h-5 w-5 text-primary-600" />
          <span>ML Model Performance Comparison</span>
        </div>
      </div>

      {/* Best Model Banner */}
      {bestModel && (
        <div className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <Target className="h-6 w-6" />
                <p className="text-sm uppercase tracking-wide opacity-90">Best Performing Model</p>
              </div>
              <p className="text-3xl font-bold">{bestModel.toUpperCase()}</p>
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90 mb-1">RMSE</p>
              <p className="text-2xl font-bold">{performance[bestModel]?.rmse?.toFixed(4)}</p>
            </div>
          </div>
        </div>
      )}

      {/* Performance Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {Object.entries(performance).map(([model, metrics], idx) => (
          <MetricCard
            key={model}
            title={model.toUpperCase()}
            value={metrics.direction_accuracy?.toFixed(1) + '%'}
            subtitle={`RMSE: ${metrics.rmse?.toFixed(4)}`}
            color={idx === 0 ? 'bg-green-50 border-green-200 text-green-900' : 'bg-gray-50 border-gray-200 text-gray-900'}
          />
        ))}
      </div>

      {/* Performance Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* RMSE Comparison */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-3 text-sm">
            Root Mean Square Error (RMSE) - Lower is Better
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="model" 
                stroke="#6b7280"
                style={{ fontSize: '11px' }}
              />
              <YAxis stroke="#6b7280" style={{ fontSize: '11px' }} />
              <Tooltip />
              <Bar dataKey="rmse" fill="#3b82f6" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Direction Accuracy Comparison */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-3 text-sm">
            Direction Accuracy (%) - Higher is Better
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="model" 
                stroke="#6b7280"
                style={{ fontSize: '11px' }}
              />
              <YAxis stroke="#6b7280" style={{ fontSize: '11px' }} />
              <Tooltip />
              <Bar dataKey="accuracy" fill="#10b981" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Model Details Table */}
      <div className="mt-6 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left font-semibold text-gray-700">Rank</th>
              <th className="px-4 py-3 text-left font-semibold text-gray-700">Model</th>
              <th className="px-4 py-3 text-right font-semibold text-gray-700">RMSE</th>
              <th className="px-4 py-3 text-right font-semibold text-gray-700">MAE</th>
              <th className="px-4 py-3 text-right font-semibold text-gray-700">MAPE (%)</th>
              <th className="px-4 py-3 text-right font-semibold text-gray-700">Direction Accuracy</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {rankedModels.map((item, idx) => (
              <tr key={item.model} className={idx === 0 ? 'bg-green-50' : 'hover:bg-gray-50'}>
                <td className="px-4 py-3">
                  {idx === 0 ? (
                    <span className="inline-flex items-center justify-center w-6 h-6 bg-green-600 text-white rounded-full text-xs font-bold">
                      1
                    </span>
                  ) : (
                    <span className="text-gray-600">{idx + 1}</span>
                  )}
                </td>
                <td className="px-4 py-3 font-medium text-gray-900">
                  {item.model.toUpperCase()}
                  {idx === 0 && <span className="ml-2 text-xs text-green-600 font-semibold">⭐ BEST</span>}
                </td>
                <td className="px-4 py-3 text-right text-gray-700">
                  {item.metrics.rmse?.toFixed(4)}
                </td>
                <td className="px-4 py-3 text-right text-gray-700">
                  {item.metrics.mae?.toFixed(4)}
                </td>
                <td className="px-4 py-3 text-right text-gray-700">
                  {item.metrics.mape?.toFixed(2)}%
                </td>
                <td className="px-4 py-3 text-right">
                  <span className={`font-semibold ${
                    item.metrics.direction_accuracy > 60 ? 'text-green-600' :
                    item.metrics.direction_accuracy > 50 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {item.metrics.direction_accuracy?.toFixed(1)}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Model Specifications */}
      <div className="mt-6">
        <button
          onClick={() => setShowSpecs(!showSpecs)}
          className="w-full flex items-center justify-between p-4 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg transition-colors"
        >
          <div className="flex items-center space-x-2">
            <Info className="h-5 w-5 text-blue-600" />
            <span className="font-semibold text-blue-900">View Model Specifications & Training Details</span>
          </div>
          {showSpecs ? <ChevronUp className="h-5 w-5 text-blue-600" /> : <ChevronDown className="h-5 w-5 text-blue-600" />}
        </button>
        
        {showSpecs && (
          <div className="mt-4 p-6 bg-white border border-gray-200 rounded-lg">
            {!rankedModels[0]?.model_specs ? (
              <div className="text-center py-8">
                <div className="text-yellow-600 mb-4">
                  <Info className="h-12 w-12 mx-auto mb-3" />
                  <h4 className="font-bold text-lg mb-2">Model Specifications Not Available</h4>
                  <p className="text-sm text-gray-600 mb-4">
                    To view detailed model specifications, please retrain the models by clicking the 
                    <strong> "Train Models & Generate Predictions"</strong> button in the ML Predictions section above.
                  </p>
                  <p className="text-xs text-gray-500">
                    The specifications will include dataset information, hyperparameters, and feature lists.
                  </p>
                </div>
              </div>
            ) : (
              rankedModels.map((item, idx) => (
              <div key={item.model} className="mb-6 pb-6 border-b last:border-b-0 last:mb-0 last:pb-0">
                <h4 className="font-bold text-lg text-gray-900 mb-4">
                  {idx + 1}. {item.model.toUpperCase()}
                  {idx === 0 && <span className="ml-2 text-xs bg-green-500 text-white px-2 py-1 rounded-full">Best Model</span>}
                </h4>
                
                {item.model_specs && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Dataset Information */}
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h5 className="font-semibold text-gray-700 mb-3 text-sm">📊 Dataset Information</h5>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Total Samples:</span>
                          <span className="font-medium text-gray-900">{item.model_specs.total_samples}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Training Samples:</span>
                          <span className="font-medium text-green-700">{item.model_specs.train_samples}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Test Samples:</span>
                          <span className="font-medium text-blue-700">{item.model_specs.test_samples}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Features Used:</span>
                          <span className="font-medium text-gray-900">{item.model_specs.n_features}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Split Ratio:</span>
                          <span className="font-medium text-gray-900">{item.model_specs.train_test_split}</span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Hyperparameters */}
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h5 className="font-semibold text-gray-700 mb-3 text-sm">⚙️ Hyperparameters</h5>
                      <div className="space-y-2 text-sm">
                        {Object.entries(item.model_specs.hyperparameters || {}).map(([key, value]) => (
                          <div key={key} className="flex justify-between">
                            <span className="text-gray-600">{key.replace(/_/g, ' ')}:</span>
                            <span className="font-medium text-gray-900">{typeof value === 'number' ? value.toFixed(3) : value.toString()}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    {/* Feature List */}
                    {item.model_specs.feature_list && item.model_specs.feature_list.length > 0 && (
                      <div className="md:col-span-2 bg-gray-50 p-4 rounded-lg">
                        <h5 className="font-semibold text-gray-700 mb-3 text-sm">🔍 Features ({item.model_specs.feature_list.length})</h5>
                        <div className="flex flex-wrap gap-2">
                          {item.model_specs.feature_list.slice(0, 20).map((feature, fidx) => (
                            <span key={fidx} className="text-xs bg-white border border-gray-300 px-2 py-1 rounded">
                              {feature}
                            </span>
                          ))}
                          {item.model_specs.feature_list.length > 20 && (
                            <span className="text-xs text-gray-500 px-2 py-1">
                              +{item.model_specs.feature_list.length - 20} more...
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )))
            }
          </div>
        )}
      </div>

      {/* Metrics Legend */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-semibold text-gray-800 mb-2 text-sm">Metrics Explained:</h4>
        <ul className="text-xs text-gray-600 space-y-1">
          <li><strong>RMSE</strong> - Root Mean Square Error: Measures average prediction error (lower is better)</li>
          <li><strong>MAE</strong> - Mean Absolute Error: Average absolute difference between predicted and actual (lower is better)</li>
          <li><strong>MAPE</strong> - Mean Absolute Percentage Error: Percentage error metric (lower is better)</li>
          <li><strong>Direction Accuracy</strong> - Percentage of correct trend predictions (higher is better)</li>
        </ul>
      </div>
    </div>
  );
};

export default ModelPerformance;
