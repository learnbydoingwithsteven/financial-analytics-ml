import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getIndicators } from '../services/api';
import { Loader2, Activity } from 'lucide-react';

const TechnicalIndicators = ({ symbol, period }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['indicators', symbol, period],
    queryFn: () => getIndicators(symbol, period),
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
      <div className="card bg-red-50 border border-red-200">
        <p className="text-red-600">Failed to load indicators</p>
      </div>
    );
  }

  const indicators = data?.indicators || {};
  const latestPrice = data?.latest_price || 0;

  const IndicatorRow = ({ label, value, condition }) => {
    const getColor = () => {
      if (condition === 'bullish') return 'text-green-600';
      if (condition === 'bearish') return 'text-red-600';
      return 'text-gray-600';
    };

    return (
      <div className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
        <span className="text-sm text-gray-600">{label}</span>
        <span className={`text-sm font-medium ${getColor()}`}>
          {value !== null && value !== undefined ? 
            (typeof value === 'number' ? value.toFixed(2) : value) : 
            'N/A'}
        </span>
      </div>
    );
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center space-x-2">
          <Activity className="h-5 w-5 text-primary-600" />
          <span>Technical Indicators</span>
        </div>
        <div className="text-sm text-gray-600">
          Latest Price: <span className="font-bold text-primary-600">${latestPrice.toFixed(2)}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Moving Averages */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-3 text-sm uppercase tracking-wide">
            📈 Moving Averages
          </h3>
          <div className="space-y-1">
            <IndicatorRow 
              label="SMA 20" 
              value={indicators.moving_averages?.sma_20}
              condition={latestPrice > indicators.moving_averages?.sma_20 ? 'bullish' : 'bearish'}
            />
            <IndicatorRow 
              label="SMA 50" 
              value={indicators.moving_averages?.sma_50}
              condition={latestPrice > indicators.moving_averages?.sma_50 ? 'bullish' : 'bearish'}
            />
            <IndicatorRow 
              label="SMA 200" 
              value={indicators.moving_averages?.sma_200}
              condition={latestPrice > indicators.moving_averages?.sma_200 ? 'bullish' : 'bearish'}
            />
            <IndicatorRow 
              label="EMA 12" 
              value={indicators.moving_averages?.ema_12}
            />
            <IndicatorRow 
              label="EMA 26" 
              value={indicators.moving_averages?.ema_26}
            />
          </div>
        </div>

        {/* Momentum Indicators */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-3 text-sm uppercase tracking-wide">
            ⚡ Momentum
          </h3>
          <div className="space-y-1">
            <IndicatorRow 
              label="RSI (14)" 
              value={indicators.momentum?.rsi}
              condition={
                indicators.momentum?.rsi < 30 ? 'bullish' :
                indicators.momentum?.rsi > 70 ? 'bearish' : 'neutral'
              }
            />
            <IndicatorRow 
              label="MACD" 
              value={indicators.momentum?.macd}
            />
            <IndicatorRow 
              label="MACD Signal" 
              value={indicators.momentum?.macd_signal}
            />
            <IndicatorRow 
              label="Stochastic K" 
              value={indicators.momentum?.stoch_k}
            />
            <IndicatorRow 
              label="Stochastic D" 
              value={indicators.momentum?.stoch_d}
            />
            <IndicatorRow 
              label="CCI (20)" 
              value={indicators.momentum?.cci}
            />
          </div>
        </div>

        {/* Volatility & Volume */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-3 text-sm uppercase tracking-wide">
            📊 Volatility & Volume
          </h3>
          <div className="space-y-1">
            <IndicatorRow 
              label="BB Upper" 
              value={indicators.volatility?.bb_upper}
            />
            <IndicatorRow 
              label="BB Middle" 
              value={indicators.volatility?.bb_middle}
            />
            <IndicatorRow 
              label="BB Lower" 
              value={indicators.volatility?.bb_lower}
            />
            <IndicatorRow 
              label="ATR (14)" 
              value={indicators.volatility?.atr}
            />
            <IndicatorRow 
              label="OBV" 
              value={indicators.volume?.obv ? 
                indicators.volume.obv.toExponential(2) : null
              }
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TechnicalIndicators;
