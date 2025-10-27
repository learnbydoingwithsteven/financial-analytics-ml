import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getSignals } from '../services/api';
import { Loader2, TrendingUp, TrendingDown, Minus, AlertCircle } from 'lucide-react';

const SignalsSummary = ({ symbol, period }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['signals', symbol, period],
    queryFn: () => getSignals(symbol, period),
  });

  if (isLoading) {
    return (
      <div className="card h-96">
        <div className="flex items-center justify-center h-full">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card h-96 bg-red-50 border border-red-200">
        <div className="flex items-center justify-center h-full">
          <p className="text-red-600">Failed to load signals</p>
        </div>
      </div>
    );
  }

  const signals = data?.signals || {};
  const overall = signals?.overall || {};

  const getSignalIcon = (signal) => {
    if (signal === 'BUY') return <TrendingUp className="h-5 w-5 text-green-600" />;
    if (signal === 'SELL') return <TrendingDown className="h-5 w-5 text-red-600" />;
    return <Minus className="h-5 w-5 text-gray-600" />;
  };

  const getSignalColor = (signal) => {
    if (signal === 'BUY') return 'bg-green-100 text-green-800 border-green-200';
    if (signal === 'SELL') return 'bg-red-100 text-red-800 border-red-200';
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getRecommendationColor = (recommendation) => {
    if (recommendation?.includes('BUY')) return 'bg-green-600';
    if (recommendation?.includes('SELL')) return 'bg-red-600';
    return 'bg-gray-600';
  };

  return (
    <div className="card h-96 flex flex-col">
      <div className="card-header">
        <div className="flex items-center space-x-2">
          <AlertCircle className="h-5 w-5 text-primary-600" />
          <span>Trading Signals</span>
        </div>
      </div>

      {/* Overall Recommendation */}
      <div className={`${getRecommendationColor(overall.recommendation)} text-white rounded-lg p-4 mb-4`}>
        <div className="text-center">
          <p className="text-sm opacity-90 mb-1">Overall Recommendation</p>
          <p className="text-2xl font-bold">{overall.recommendation || 'N/A'}</p>
          <div className="flex justify-center space-x-4 mt-3 text-sm">
            <div>
              <p className="opacity-75">Confidence</p>
              <p className="font-semibold">{overall.confidence || 0}%</p>
            </div>
            <div className="border-l border-white opacity-50"></div>
            <div>
              <p className="opacity-75">Buy Signals</p>
              <p className="font-semibold">{overall.buy_signals?.toFixed(1) || 0}</p>
            </div>
            <div className="border-l border-white opacity-50"></div>
            <div>
              <p className="opacity-75">Sell Signals</p>
              <p className="font-semibold">{overall.sell_signals?.toFixed(1) || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Individual Signals */}
      <div className="flex-1 overflow-y-auto space-y-2">
        {Object.entries(signals)
          .filter(([key]) => key !== 'overall')
          .map(([indicator, signal]) => (
            <div
              key={indicator}
              className={`border rounded-lg p-3 ${getSignalColor(signal.signal)}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  {getSignalIcon(signal.signal)}
                  <div>
                    <p className="font-medium text-sm capitalize">
                      {indicator.replace('_', ' ')}
                    </p>
                    <p className="text-xs mt-1 opacity-75">
                      {signal.reason}
                    </p>
                  </div>
                </div>
                <span className={`badge ${
                  signal.strength === 'strong' ? 'badge-success' :
                  signal.strength === 'medium' ? 'badge-warning' : 'badge-info'
                }`}>
                  {signal.strength}
                </span>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};

export default SignalsSummary;
