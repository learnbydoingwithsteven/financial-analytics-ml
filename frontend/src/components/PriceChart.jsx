import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, ReferenceDot } from 'recharts';
import { getData, getIndicators, getSignals } from '../services/api';
import { Loader2, TrendingUp, Eye, EyeOff, TrendingDown as SellIcon, TrendingUp as BuyIcon } from 'lucide-react';
import { format } from 'date-fns';

const PriceChart = ({ symbol, period }) => {
  const [showIndicators, setShowIndicators] = useState(false);
  const [selectedIndicators, setSelectedIndicators] = useState({
    sma20: true,
    sma50: true,
    bb: false,
    ema12: false
  });
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['data', symbol, period],
    queryFn: () => getData(symbol, period),
  });

  const { data: indicatorData } = useQuery({
    queryKey: ['indicators-chart', symbol, period],
    queryFn: () => getIndicators(symbol, period),
    enabled: showIndicators,
  });

  const { data: signalsData } = useQuery({
    queryKey: ['signals-chart', symbol, period],
    queryFn: () => getSignals(symbol, period),
    enabled: showIndicators,
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
          <p className="text-red-600">Failed to load price data</p>
        </div>
      </div>
    );
  }

  // Format data for chart
  const chartData = data?.data?.map((item, idx) => {
    const baseData = {
      date: format(new Date(item.date), 'MMM dd'),
      price: item.close,
      fullDate: item.date
    };

    // Add indicator time series data if available
    if (showIndicators && indicatorData?.data) {
      const indicatorItem = indicatorData.data[idx];
      if (indicatorItem) {
        baseData.sma_20 = indicatorItem.sma_20;
        baseData.sma_50 = indicatorItem.sma_50;
        baseData.ema_12 = indicatorItem.ema_12;
        baseData.bb_upper = indicatorItem.bb_upper;
        baseData.bb_middle = indicatorItem.bb_middle;
        baseData.bb_lower = indicatorItem.bb_lower;
      }
    }

    return baseData;
  }) || [];

  // Extract signal information
  const signals = signalsData?.signals || {};
  const overallSignal = signals?.overall?.recommendation;
  
  // Generate signal markers (simplified - mark first and last points with signals)
  const buySignalPoints = [];
  const sellSignalPoints = [];
  
  if (showIndicators && chartData.length > 0 && overallSignal) {
    // Add signal at the latest data point
    const latestPoint = chartData[chartData.length - 1];
    if (overallSignal === 'BUY' || overallSignal === 'STRONG BUY') {
      buySignalPoints.push({ ...latestPoint, signal: 'BUY' });
    } else if (overallSignal === 'SELL' || overallSignal === 'STRONG SELL') {
      sellSignalPoints.push({ ...latestPoint, signal: 'SELL' });
    }
    
    // Add historical signals based on MA crossovers (simplified)
    if (signals.ma_trend?.signal === 'BUY') {
      const midPoint = chartData[Math.floor(chartData.length / 2)];
      buySignalPoints.push({ ...midPoint, signal: 'BUY' });
    }
    if (signals.ma_trend?.signal === 'SELL') {
      const midPoint = chartData[Math.floor(chartData.length / 2)];
      sellSignalPoints.push({ ...midPoint, signal: 'SELL' });
    }
  }

  // Calculate price change
  const latestPrice = data?.data?.[data.data.length - 1]?.close || 0;
  const firstPrice = data?.data?.[0]?.close || 0;
  const priceChange = latestPrice - firstPrice;
  const priceChangePercent = ((priceChange / firstPrice) * 100).toFixed(2);
  const isPositive = priceChange >= 0;

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between mb-4">
          <div className="card-header-title">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-primary-600" />
              <span>Price Chart</span>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            {showIndicators && (
              <div className="flex items-center space-x-2 text-xs">
                <label className="flex items-center space-x-1 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedIndicators.sma20}
                    onChange={(e) => setSelectedIndicators({...selectedIndicators, sma20: e.target.checked})}
                    className="rounded"
                  />
                  <span className="text-orange-600">SMA 20</span>
                </label>
                <label className="flex items-center space-x-1 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedIndicators.sma50}
                    onChange={(e) => setSelectedIndicators({...selectedIndicators, sma50: e.target.checked})}
                    className="rounded"
                  />
                  <span className="text-purple-600">SMA 50</span>
                </label>
                <label className="flex items-center space-x-1 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedIndicators.bb}
                    onChange={(e) => setSelectedIndicators({...selectedIndicators, bb: e.target.checked})}
                    className="rounded"
                  />
                  <span className="text-blue-600">Bollinger</span>
                </label>
                <label className="flex items-center space-x-1 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedIndicators.ema12}
                    onChange={(e) => setSelectedIndicators({...selectedIndicators, ema12: e.target.checked})}
                    className="rounded"
                  />
                  <span className="text-green-600">EMA 12</span>
                </label>
              </div>
            )}
            <button
              onClick={() => setShowIndicators(!showIndicators)}
              className="flex items-center space-x-2 px-4 py-2 bg-primary-50 text-primary-700 hover:bg-primary-100 rounded-lg transition-colors text-sm font-medium"
            >
              {showIndicators ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              <span>{showIndicators ? 'Hide' : 'Show'} Indicators</span>
            </button>
          </div>
        </div>
        <div className="text-right mt-2">
          <div className="text-2xl font-bold">
            ${latestPrice.toFixed(2)}
          </div>
          <div className={`text-sm font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {isPositive ? '+' : ''}{priceChange.toFixed(2)} ({isPositive ? '+' : ''}{priceChangePercent}%)
          </div>
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="date" 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            domain={['auto', 'auto']}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="price" 
            stroke="#0ea5e9" 
            strokeWidth={2}
            dot={false}
            name="Price"
          />
          {showIndicators && selectedIndicators.sma20 && (
            <Line
              type="monotone"
              dataKey="sma_20"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={false}
              name="SMA 20"
              connectNulls
            />
          )}
          {showIndicators && selectedIndicators.sma50 && (
            <Line
              type="monotone"
              dataKey="sma_50"
              stroke="#8b5cf6"
              strokeWidth={2}
              dot={false}
              name="SMA 50"
              connectNulls
            />
          )}
          {showIndicators && selectedIndicators.ema12 && (
            <Line
              type="monotone"
              dataKey="ema_12"
              stroke="#10b981"
              strokeWidth={2}
              dot={false}
              name="EMA 12"
              strokeDasharray="3 3"
              connectNulls
            />
          )}
          {showIndicators && selectedIndicators.bb && (
            <>
              <Line
                type="monotone"
                dataKey="bb_upper"
                stroke="#3b82f6"
                strokeWidth={1}
                dot={false}
                name="BB Upper"
                strokeDasharray="2 2"
                connectNulls
              />
              <Line
                type="monotone"
                dataKey="bb_middle"
                stroke="#60a5fa"
                strokeWidth={1}
                dot={false}
                name="BB Middle"
                strokeDasharray="2 2"
                connectNulls
              />
              <Line
                type="monotone"
                dataKey="bb_lower"
                stroke="#3b82f6"
                strokeWidth={1}
                dot={false}
                name="BB Lower"
                strokeDasharray="2 2"
                connectNulls
              />
            </>
          )}
          {/* Buy Signals */}
          {showIndicators && buySignalPoints.map((point, idx) => (
            <ReferenceDot
              key={`buy-${idx}`}
              x={point.date}
              y={point.price}
              r={8}
              fill="#10b981"
              stroke="#fff"
              strokeWidth={2}
              label={{ value: '▲ BUY', position: 'top', fill: '#10b981', fontSize: 10, fontWeight: 'bold' }}
            />
          ))}
          {/* Sell Signals */}
          {showIndicators && sellSignalPoints.map((point, idx) => (
            <ReferenceDot
              key={`sell-${idx}`}
              x={point.date}
              y={point.price}
              r={8}
              fill="#ef4444"
              stroke="#fff"
              strokeWidth={2}
              label={{ value: '▼ SELL', position: 'bottom', fill: '#ef4444', fontSize: 10, fontWeight: 'bold' }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      
      {/* Signal Legend */}
      {showIndicators && (buySignalPoints.length > 0 || sellSignalPoints.length > 0) && (
        <div className="mt-4 p-3 bg-gray-50 border border-gray-200 rounded-lg">
          <div className="flex items-center justify-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 rounded-full bg-green-500 border-2 border-white"></div>
              <span className="text-gray-700">
                <span className="font-semibold text-green-600">▲ BUY Signal</span>
                {signals.overall && ` - ${signals.overall.buy_signals} indicators`}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 rounded-full bg-red-500 border-2 border-white"></div>
              <span className="text-gray-700">
                <span className="font-semibold text-red-600">▼ SELL Signal</span>
                {signals.overall && ` - ${signals.overall.sell_signals} indicators`}
              </span>
            </div>
            <div className="text-gray-600">
              Overall: <span className={`font-bold ${
                overallSignal === 'BUY' || overallSignal === 'STRONG BUY' ? 'text-green-600' :
                overallSignal === 'SELL' || overallSignal === 'STRONG SELL' ? 'text-red-600' :
                'text-yellow-600'
              }`}>{overallSignal}</span>
              {signals.overall && ` (${signals.overall.confidence.toFixed(1)}% confidence)`}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PriceChart;
