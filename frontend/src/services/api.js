/**
 * API Service for Financial Analytics Dashboard
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for ML training
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Get list of all assets
 */
export const getAssets = async () => {
  const response = await api.get('/assets');
  return response.data;
};

/**
 * Get historical data for a symbol
 */
export const getData = async (symbol, period = '1y') => {
  const response = await api.get(`/data/${symbol}`, {
    params: { period }
  });
  return response.data;
};

/**
 * Get technical indicators for a symbol
 */
export const getIndicators = async (symbol, period = '1y') => {
  const response = await api.get(`/indicators/${symbol}`, {
    params: { period }
  });
  return response.data;
};

/**
 * Get buy/sell signals for a symbol
 */
export const getSignals = async (symbol, period = '1y') => {
  const response = await api.get(`/signals/${symbol}`, {
    params: { period }
  });
  return response.data;
};

/**
 * Train ML models for a symbol
 */
export const trainModels = async (symbol, period = '2y', params = {}) => {
  const requestBody = {
    symbol,
    period,
    ...params
  };
  const response = await api.post('/train', requestBody);
  return response.data;
};

/**
 * Get ML predictions for a symbol
 */
export const getPredictions = async (symbol, model = 'ensemble') => {
  const response = await api.get(`/predictions/${symbol}`, {
    params: { model }
  });
  return response.data;
};

/**
 * Get model performance comparison
 */
export const getModelPerformance = async (symbol) => {
  const response = await api.get(`/models/performance/${symbol}`);
  return response.data;
};

/**
 * Run historical backtest with multiple configurations
 */
export const runBacktest = async (symbol, period, configs) => {
  const response = await api.post('/backtest', {
    symbol,
    period,
    configs
  });
  return response.data;
};

/**
 * Predict future prices using best configuration
 */
export const predictFuture = async (symbol, period, bestConfig, predictionHorizon) => {
  const response = await api.post('/predict-future', {
    symbol,
    period,
    best_config: bestConfig,
    prediction_horizon: predictionHorizon
  });
  return response.data;
};

/**
 * Get latest price for a symbol
 */
export const getLatestPrice = async (symbol) => {
  const response = await api.get(`/latest/${symbol}`);
  return response.data;
};

export default api;
