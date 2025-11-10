# Financial Analytics Dashboard

A comprehensive full-stack financial analytics application with ML predictions and technical indicators.

## Features

### Assets Tracked
- **EUR/CNY** exchange rate
- **Gold** prices (GC=F)
- **US Bonds** (TLT - 20+ Year Treasury Bond ETF)
- **China Bonds** (CBON - China Government Bond)
- **US Stock Indexes**: S&P 500 (^GSPC), Dow Jones (^DJI), NASDAQ (^IXIC)
- **China Stock Indexes**: Shanghai Composite (000001.SS), Shenzhen Component (399001.SZ), Hang Seng (^HSI)

### Technical Indicators with Buy/Sell Signals
- **Trend Indicators**: SMA (20, 50, 200), EMA (12, 26), MACD
- **Momentum Indicators**: RSI, Stochastic Oscillator, CCI
- **Volatility Indicators**: Bollinger Bands, ATR
- **Volume Indicators**: OBV, Volume SMA
- **Support/Resistance**: Pivot Points, Fibonacci Retracements

### Machine Learning Predictions
- **Time Horizons**: 1 month, 2 months, 3 months, 6 months
- **Algorithms**:
  1. **LSTM** (Long Short-Term Memory Neural Network)
  2. **Random Forest** Regressor
  3. **XGBoost** (Extreme Gradient Boosting)
  4. **Prophet** (Facebook's time series forecasting)
  5. **ARIMA** (AutoRegressive Integrated Moving Average)
  6. **Ensemble Model** (Combined predictions)

### Dynamic Algorithm Valuation
- Real-time accuracy tracking
- RMSE, MAE, MAPE metrics
- Confidence intervals
- Historical performance comparison
- Best performing model recommendation

## Tech Stack

### Backend
- **Python 3.9+** with FastAPI
- **yfinance** - Free Yahoo Finance data
- **pandas-ta** / **ta-lib** - Technical indicators
- **scikit-learn** - ML models
- **tensorflow/keras** - Deep learning (LSTM)
- **xgboost** - Gradient boosting
- **prophet** - Time series forecasting
- **statsmodels** - ARIMA

### Frontend
- **React 18** with TypeScript
- **Vite** - Fast build tool
- **TailwindCSS** - Styling
- **Recharts** / **Plotly.js** - Charts
- **Axios** - API calls
- **React Query** - Data fetching

### Database
- **SQLite** - Lightweight data storage for cache

## Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py

cd backend
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev

cd frontend
npm run dev
```

## Usage

1. Start backend server: `http://localhost:8001`
2. Start frontend: `http://localhost:5173`
3. Access dashboard at `http://localhost:5173`

## Features

- **Real-time Data**: Fetch live market data from Yahoo Finance
- **Technical Indicators**: 15+ indicators (SMA, RSI, MACD, Bollinger Bands, etc.)
- **Trading Signals**: Buy/Sell/Hold recommendations with confidence scores
- **ML Predictions**: 6 models (LSTM, Random Forest, XGBoost, Prophet, ARIMA, Ensemble)
- **Interactive Charts**: Click to expand indicator details and historical values
- **On-Demand Training**: Click "Predict" button to train models and generate forecasts

## Free Data Sources
- **Yahoo Finance** (via yfinance) - No API key required
- **Alpha Vantage** (optional, free tier) - 5 calls/minute, 500/day

## API Endpoints

- `GET /api/assets` - List all tracked assets
- `GET /api/data/{symbol}` - Historical data for symbol
- `GET /api/indicators/{symbol}` - Technical indicators
- `GET /api/signals/{symbol}` - Buy/sell signals
- `GET /api/predictions/{symbol}` - ML predictions
- `GET /api/algorithms/performance` - Algorithm comparison

## License
MIT License
