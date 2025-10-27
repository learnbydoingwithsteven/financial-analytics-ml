import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TrendingUp, DollarSign, BarChart3, Activity } from 'lucide-react';
import AssetSelector from './components/AssetSelector';
import PriceChart from './components/PriceChart';
import TechnicalIndicators from './components/TechnicalIndicators';
import SignalsSummary from './components/SignalsSummary';
import AdvancedBacktesting from './components/AdvancedBacktesting';
import ModelPerformance from './components/ModelPerformance';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  const [selectedSymbol, setSelectedSymbol] = useState('EURCNY=X');
  const [period, setPeriod] = useState('1y');

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        {/* Header */}
        <header className="bg-white shadow-md border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="bg-primary-600 rounded-lg p-2">
                  <TrendingUp className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">
                    Financial Analytics Dashboard
                  </h1>
                  <p className="text-sm text-gray-600 mt-1">
                    Real-time market data, technical indicators & ML predictions
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-lg">
                  <Activity className="h-5 w-5 text-green-600 animate-pulse" />
                  <span className="text-sm font-medium text-gray-700">Live Data</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Controls */}
          <div className="mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <AssetSelector 
                selectedSymbol={selectedSymbol}
                onSymbolChange={setSelectedSymbol}
              />
              
              <div className="card">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Time Period
                </label>
                <select
                  value={period}
                  onChange={(e) => setPeriod(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="1mo">1 Month</option>
                  <option value="3mo">3 Months</option>
                  <option value="6mo">6 Months</option>
                  <option value="1y">1 Year</option>
                  <option value="2y">2 Years</option>
                  <option value="5y">5 Years</option>
                </select>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm opacity-90">Market</p>
                  <p className="text-2xl font-bold mt-1">Live</p>
                </div>
                <BarChart3 className="h-10 w-10 opacity-80" />
              </div>
            </div>

            <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm opacity-90">Signals</p>
                  <p className="text-2xl font-bold mt-1">Active</p>
                </div>
                <Activity className="h-10 w-10 opacity-80" />
              </div>
            </div>

            <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm opacity-90">ML Models</p>
                  <p className="text-2xl font-bold mt-1">6 Active</p>
                </div>
                <TrendingUp className="h-10 w-10 opacity-80" />
              </div>
            </div>

            <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm opacity-90">Indicators</p>
                  <p className="text-2xl font-bold mt-1">15+</p>
                </div>
                <DollarSign className="h-10 w-10 opacity-80" />
              </div>
            </div>
          </div>

          {/* Price Chart & Signals */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <div className="lg:col-span-2">
              <PriceChart symbol={selectedSymbol} period={period} />
            </div>
            <div>
              <SignalsSummary symbol={selectedSymbol} period={period} />
            </div>
          </div>

          {/* Technical Indicators */}
          <div className="mb-6">
            <TechnicalIndicators symbol={selectedSymbol} period={period} />
          </div>

          {/* Advanced Backtesting & ML Predictions */}
          <div className="mb-6">
            <AdvancedBacktesting symbol={selectedSymbol} period={period} />
          </div>

          {/* Model Performance */}
          <div className="mb-6">
            <ModelPerformance symbol={selectedSymbol} />
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <p className="text-center text-sm text-gray-600">
              © 2024 Financial Analytics Dashboard | Data from Yahoo Finance | 
              <span className="font-medium"> Free & Open Source</span>
            </p>
          </div>
        </footer>
      </div>
    </QueryClientProvider>
  );
}

export default App;
