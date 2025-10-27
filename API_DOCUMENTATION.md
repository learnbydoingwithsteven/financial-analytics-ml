# Financial Analytics API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for local use.

---

## Endpoints

### 1. Health Check

**GET /** 

Get API status and version information.

**Response:**
```json
{
  "message": "Financial Analytics API",
  "version": "1.0.0",
  "endpoints": {
    "assets": "/api/assets",
    "data": "/api/data/{symbol}",
    ...
  }
}
```

---

### 2. Get Assets List

**GET /api/assets**

Retrieve list of all tracked financial assets.

**Response:**
```json
{
  "assets": [
    {
      "symbol": "EURCNY=X",
      "name": "EUR/CNY",
      "category": "forex",
      "exchange": "FX"
    },
    ...
  ]
}
```

**Categories:**
- `forex` - Currency exchange rates
- `commodity` - Commodities (Gold, etc.)
- `us_bond` - US Government Bonds
- `cn_bond` - China Government Bonds
- `us_index` - US Stock Indexes
- `cn_index` - China Stock Indexes

---

### 3. Get Historical Data

**GET /api/data/{symbol}**

Fetch historical OHLCV data for a symbol.

**Parameters:**
- `symbol` (path) - Asset symbol (e.g., "EURCNY=X")
- `period` (query, optional) - Time period (default: "1y")
  - Options: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"

**Example:**
```bash
GET /api/data/EURCNY=X?period=6mo
```

**Response:**
```json
{
  "symbol": "EURCNY=X",
  "name": "EUR/CNY",
  "period": "6mo",
  "records": 126,
  "data": [
    {
      "date": "2024-04-25",
      "open": 7.8234,
      "high": 7.8567,
      "low": 7.8123,
      "close": 7.8456,
      "volume": 0
    },
    ...
  ]
}
```

---

### 4. Get Technical Indicators

**GET /api/indicators/{symbol}**

Calculate technical indicators for a symbol.

**Parameters:**
- `symbol` (path) - Asset symbol
- `period` (query, optional) - Time period (default: "1y")

**Example:**
```bash
GET /api/indicators/^GSPC?period=1y
```

**Response:**
```json
{
  "symbol": "^GSPC",
  "name": "S&P 500",
  "latest_price": 4567.89,
  "indicators": {
    "moving_averages": {
      "sma_20": 4550.23,
      "sma_50": 4523.45,
      "sma_200": 4478.90,
      "ema_12": 4562.34,
      "ema_26": 4545.67
    },
    "momentum": {
      "rsi": 58.34,
      "macd": 12.45,
      "macd_signal": 10.23,
      "stoch_k": 62.5,
      "stoch_d": 60.8,
      "cci": 45.67
    },
    "volatility": {
      "bb_upper": 4620.12,
      "bb_middle": 4567.89,
      "bb_lower": 4515.66,
      "atr": 45.23
    },
    "volume": {
      "obv": 12345678900
    }
  }
}
```

**Indicators Explained:**

**Moving Averages:**
- `sma_20/50/200` - Simple Moving Average
- `ema_12/26` - Exponential Moving Average

**Momentum:**
- `rsi` - Relative Strength Index (0-100)
- `macd` - Moving Average Convergence Divergence
- `macd_signal` - MACD Signal Line
- `stoch_k` - Stochastic K (0-100)
- `stoch_d` - Stochastic D (0-100)
- `cci` - Commodity Channel Index

**Volatility:**
- `bb_upper/middle/lower` - Bollinger Bands
- `atr` - Average True Range

**Volume:**
- `obv` - On-Balance Volume

---

### 5. Get Trading Signals

**GET /api/signals/{symbol}**

Generate buy/sell/hold signals based on technical indicators.

**Parameters:**
- `symbol` (path) - Asset symbol
- `period` (query, optional) - Time period (default: "1y")

**Example:**
```bash
GET /api/signals/GC=F?period=1y
```

**Response:**
```json
{
  "symbol": "GC=F",
  "name": "Gold Futures",
  "signals": {
    "ma_trend": {
      "signal": "BUY",
      "strength": "strong",
      "reason": "Price above SMA 20 and 50"
    },
    "macd": {
      "signal": "BUY",
      "strength": "medium",
      "reason": "MACD above signal line"
    },
    "rsi": {
      "signal": "NEUTRAL",
      "strength": "neutral",
      "reason": "RSI neutral at 55.3"
    },
    "bollinger": {
      "signal": "NEUTRAL",
      "strength": "neutral",
      "reason": "Price within bands"
    },
    "stochastic": {
      "signal": "BUY",
      "strength": "medium",
      "reason": "Stochastic oversold and turning up"
    },
    "overall": {
      "recommendation": "BUY",
      "buy_signals": 4.5,
      "sell_signals": 0.5,
      "total_signals": 7,
      "buy_percentage": 64.3,
      "sell_percentage": 7.1,
      "confidence": 64.3
    }
  }
}
```

**Signal Types:**
- `BUY` - Bullish signal
- `SELL` - Bearish signal
- `NEUTRAL` - No clear signal

**Strength Levels:**
- `strong` - High confidence
- `medium` - Medium confidence
- `weak` - Low confidence

**Overall Recommendations:**
- `STRONG BUY` - Buy percentage > 60%
- `BUY` - Buy percentage 50-60%
- `HOLD` - Mixed signals
- `SELL` - Sell percentage 50-60%
- `STRONG SELL` - Sell percentage > 60%

---

### 6. Train ML Models

**POST /api/train**

Train machine learning models for a symbol.

**Request Body:**
```json
{
  "symbol": "EURCNY=X",
  "period": "2y"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/train \
  -H "Content-Type: application/json" \
  -d '{"symbol": "EURCNY=X", "period": "2y"}'
```

**Response:**
```json
{
  "symbol": "EURCNY=X",
  "name": "EUR/CNY",
  "training_results": {
    "lstm": {
      "success": true,
      "model": "LSTM",
      "metrics": {
        "rmse": 0.0234,
        "mae": 0.0189,
        "mape": 0.24,
        "direction_accuracy": 62.5
      },
      "training_loss": 0.0005,
      "validation_loss": 0.0006
    },
    "random_forest": {
      "success": true,
      "model": "Random Forest",
      "metrics": {
        "rmse": 0.0198,
        "mae": 0.0156,
        "mape": 0.20,
        "direction_accuracy": 65.8
      },
      "top_features": [
        {"feature": "close_lag_1", "importance": 0.234},
        {"feature": "ma_20", "importance": 0.189}
      ]
    },
    ...
  }
}
```

**Note:** Training may take 30-60 seconds depending on data size and models.

---

### 7. Get ML Predictions

**GET /api/predictions/{symbol}**

Get price predictions from all ML models for multiple time horizons.

**Parameters:**
- `symbol` (path) - Asset symbol
- `model` (query, optional) - Specific model (default: all models)

**Example:**
```bash
GET /api/predictions/^GSPC
```

**Response:**
```json
{
  "symbol": "^GSPC",
  "name": "S&P 500",
  "predictions": {
    "1m": {
      "lstm": {
        "success": true,
        "model": "LSTM",
        "predictions": [4567.89, 4578.12, 4589.34, ...],
        "lower_bound": [4520.45, 4530.67, ...],
        "upper_bound": [4615.33, 4625.57, ...],
        "horizon": 21
      },
      "random_forest": {...},
      "xgboost": {...},
      "prophet": {...},
      "ensemble": {
        "success": true,
        "model": "ensemble",
        "predictions": [4567.89, 4579.23, ...],
        "lower_bound": [...],
        "upper_bound": [...],
        "horizon": 21,
        "models_used": ["lstm", "random_forest", "xgboost", "prophet"],
        "individual_predictions": {...}
      }
    },
    "2m": {...},
    "3m": {...},
    "6m": {...}
  }
}
```

**Time Horizons:**
- `1m` - 1 month (21 trading days)
- `2m` - 2 months (42 trading days)
- `3m` - 3 months (63 trading days)
- `6m` - 6 months (126 trading days)

**Models:**
- `lstm` - Long Short-Term Memory neural network
- `random_forest` - Random Forest regression
- `xgboost` - XGBoost gradient boosting
- `prophet` - Facebook Prophet time series
- `ensemble` - Weighted combination of all models

---

### 8. Get Model Performance

**GET /api/models/performance/{symbol}**

Compare performance metrics of all ML models.

**Parameters:**
- `symbol` (path) - Asset symbol

**Example:**
```bash
GET /api/models/performance/TLT
```

**Response:**
```json
{
  "symbol": "TLT",
  "name": "US 20+ Year Treasury Bond ETF",
  "performance": {
    "performance": {
      "lstm": {
        "rmse": 0.0234,
        "mae": 0.0189,
        "mape": 0.24,
        "direction_accuracy": 62.5,
        "is_trained": true
      },
      "random_forest": {...},
      "xgboost": {...},
      "prophet": {...}
    },
    "best_model": "xgboost",
    "ranked_models": [
      {
        "model": "xgboost",
        "metrics": {
          "rmse": 0.0187,
          "mae": 0.0145,
          "mape": 0.19,
          "direction_accuracy": 68.2
        }
      },
      ...
    ]
  }
}
```

**Metrics Explained:**
- `rmse` - Root Mean Square Error (lower is better)
- `mae` - Mean Absolute Error (lower is better)
- `mape` - Mean Absolute Percentage Error (lower is better)
- `direction_accuracy` - % of correct trend predictions (higher is better)

---

### 9. Get Latest Price

**GET /api/latest/{symbol}**

Get the most recent price for a symbol.

**Parameters:**
- `symbol` (path) - Asset symbol

**Example:**
```bash
GET /api/latest/000001.SS
```

**Response:**
```json
{
  "symbol": "000001.SS",
  "name": "Shanghai Composite",
  "price": 3245.67
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `404` - Symbol or resource not found
- `500` - Internal server error (data fetch failed, calculation error, etc.)

---

## Rate Limiting

No rate limiting for local use. Yahoo Finance has built-in rate limiting:
- Reasonable use: ~1-2 requests per second
- Excessive use may result in temporary blocks

---

## Data Source

All market data is fetched from **Yahoo Finance** via the `yfinance` library:
- Free and open source
- No API key required
- Real-time and historical data
- Covers global markets

---

## Interactive Documentation

Visit **http://localhost:8000/docs** for interactive API documentation where you can:
- View all endpoints
- See request/response schemas
- Try API calls directly
- Download OpenAPI specification

---

## Code Examples

### Python

```python
import requests

# Get signals
response = requests.get("http://localhost:8000/api/signals/EURCNY=X")
data = response.json()
print(f"Recommendation: {data['signals']['overall']['recommendation']}")

# Train models
response = requests.post(
    "http://localhost:8000/api/train",
    json={"symbol": "^GSPC", "period": "2y"}
)
print(response.json())
```

### JavaScript

```javascript
// Get predictions
fetch('http://localhost:8000/api/predictions/GC=F')
  .then(response => response.json())
  .then(data => {
    console.log('1-month prediction:', data.predictions['1m'].ensemble);
  });
```

### cURL

```bash
# Get technical indicators
curl "http://localhost:8000/api/indicators/TLT?period=1y"

# Train models
curl -X POST http://localhost:8000/api/train \
  -H "Content-Type: application/json" \
  -d '{"symbol": "CBON", "period": "2y"}'
```

---

## Best Practices

1. **Cache responses** - Data updates every hour, cache accordingly
2. **Handle errors** - Always check response status codes
3. **Use appropriate periods** - Longer periods for ML training (2y), shorter for quick analysis (1mo)
4. **Train models once** - Training is expensive, cache results
5. **Batch requests** - If fetching multiple symbols, space out requests

---

## Support

For issues or questions:
- Check **TROUBLESHOOTING.md** for common problems
- Review **INSTALLATION.md** for setup help
- Check API logs in terminal for error details
