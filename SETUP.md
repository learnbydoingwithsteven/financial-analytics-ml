# Financial Analytics Dashboard - Setup Guide

## Quick Start

### Prerequisites
- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- Internet connection for data fetching

### Installation

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The backend API will start at `http://localhost:8000`

#### 2. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start at `http://localhost:5173`

### Access the Dashboard

Open your browser and navigate to: **http://localhost:5173**

## Features Overview

### 1. Asset Tracking
- **EUR/CNY** exchange rate
- **Gold** (GC=F)
- **US Bonds** (TLT, IEF)
- **China Bonds** (CBON)
- **US Indexes** (S&P 500, Dow Jones, NASDAQ)
- **China Indexes** (Shanghai Composite, Shenzhen Component, Hang Seng)

### 2. Technical Indicators
- **Trend**: SMA (20, 50, 200), EMA (12, 26), MACD
- **Momentum**: RSI, Stochastic, CCI
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV

### 3. Buy/Sell Signals
- Automated signal generation
- Multiple indicator confirmation
- Confidence scoring
- Real-time recommendations

### 4. ML Predictions (6 Models)
- **LSTM** - Deep learning neural network
- **Random Forest** - Ensemble tree model
- **XGBoost** - Gradient boosting
- **Prophet** - Time series forecasting
- **ARIMA** - Statistical model
- **Ensemble** - Combined predictions

### 5. Time Horizons
- 1 month (21 trading days)
- 2 months (42 trading days)
- 3 months (63 trading days)
- 6 months (126 trading days)

### 6. Model Performance
- RMSE, MAE, MAPE metrics
- Direction accuracy
- Model comparison
- Best model recommendation

## Data Sources

### Yahoo Finance (Free, No API Key)
All market data is fetched from Yahoo Finance via the `yfinance` library:
- Real-time and historical data
- No rate limits for reasonable use
- No API key required

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError`
**Solution**: Make sure you installed all dependencies: `pip install -r requirements.txt`

**Issue**: TensorFlow not installing on Apple Silicon
**Solution**: Use: `pip install tensorflow-macos tensorflow-metal`

**Issue**: Port 8000 already in use
**Solution**: Change port in `backend/config.py`

### Frontend Issues

**Issue**: `npm install` fails
**Solution**: Delete `node_modules` and `package-lock.json`, then run `npm install` again

**Issue**: CORS errors
**Solution**: Make sure backend is running on port 8000

**Issue**: API connection failed
**Solution**: Check that backend is running at `http://localhost:8000`

## Development

### Backend Development
- FastAPI auto-reloads on code changes
- API docs available at `http://localhost:8000/docs`

### Frontend Development
- Vite provides hot module replacement
- Changes reflect immediately in browser

## Production Deployment

### Backend
```bash
cd backend
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm run build
# Serve the dist folder with any static server
```

## Performance Optimization

### Backend
- Implement caching for frequently accessed data
- Use background tasks for model training
- Consider Redis for session storage

### Frontend
- Enable React production build
- Implement lazy loading for components
- Use service workers for offline support

## API Documentation

Full API documentation available at: `http://localhost:8000/docs`

Key endpoints:
- `GET /api/assets` - List all assets
- `GET /api/data/{symbol}` - Historical data
- `GET /api/indicators/{symbol}` - Technical indicators
- `GET /api/signals/{symbol}` - Buy/sell signals
- `POST /api/train` - Train ML models
- `GET /api/predictions/{symbol}` - ML predictions
- `GET /api/models/performance/{symbol}` - Model comparison

## License

MIT License - Free to use and modify

## Support

For issues or questions, please open an issue on GitHub.
