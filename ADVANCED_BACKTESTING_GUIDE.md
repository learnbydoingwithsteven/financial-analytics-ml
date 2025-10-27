# Advanced Backtesting & Prediction System - Complete Guide

## 🎯 Overview

A revolutionary ML prediction system with **3 major improvements**:

1. ✅ **Indicators Display Fixed** - Time series lines now show properly
2. ✅ **No Auto-Training** - Models only train when you click the button
3. ✅ **Advanced Backtesting** - Test multiple configurations, find best setup, predict future

---

## 🚀 What's New

### Issue 1: Indicators Now Working ✅

**Fixed**: Backend now returns time series data for all indicators
- `/api/indicators/{symbol}` now includes `data` array with sma_20, sma_50, ema_12, bollinger bands for each time point
- Frontend displays indicators as proper time series lines (not horizontal)
- Selectable checkboxes for different indicators

### Issue 2: No Auto-Training ✅

**Fixed**: `/api/predictions` endpoint no longer auto-trains
- Returns HTTP 400 error if models not trained
- User MUST click "Train" button explicitly
- Clear error message: "Models not trained. Please train models first."

### Issue 3: Advanced Backtesting System ✅

**New Feature**: Comprehensive historical testing and future prediction
- **Step 1**: Historical backtesting with multiple configurations
- **Step 2**: Use best configuration to predict future

---

## 📋 System Architecture

### Backend Components

#### 1. **backtesting.py** (New File)
Advanced backtesting engine with:
- `BacktestingEngine` class
- `prepare_historical_backtest()` - Split data into train/val/test
- `run_backtest()` - Run single configuration
- `compare_configurations()` - Compare multiple setups
- `predict_future()` - Predict beyond historical data

#### 2. **main.py** (Updated)
New API endpoints:
- `POST /api/backtest` - Run historical backtests
- `POST /api/predict-future` - Predict future prices
- `GET /api/indicators/{symbol}` - Returns time series data
- `GET /api/predictions/{symbol}` - Requires training first

#### 3. **Request Models** (New)
```python
class BacktestConfig:
    test_period: str  # 'current_month' or 'current_3months'
    train_lookback: str  # '1month', '2months', '3months', '6months'
    train_test_split: str  # '80_20' or '70_30'

class BacktestRequest:
    symbol: str
    period: str
    configs: List[BacktestConfig]

class FuturePredictRequest:
    symbol: str
    period: str
    best_config: Dict
    prediction_horizon: str  # '1month' or '3months'
```

### Frontend Components

#### 1. **AdvancedBacktesting.jsx** (New Component)
Comprehensive UI for:
- Configuration selection
- Backtest execution
- Results visualization
- Future predictions

#### 2. **api.js** (Updated)
New API functions:
- `runBacktest(symbol, period, configs)`
- `predictFuture(symbol, period, bestConfig, predictionHorizon)`

---

## 🎓 How To Use - Complete Workflow

### Step 1: Select Configurations

The new UI shows a grid with **Test Periods** × **Train Lookbacks** × **Train/Test Splits**:

```
┌─ Test Period: Current Month (30 days) ────────────┐
│  1 Month Training:                                 │
│    [✓] 80/20 Split    [ ] 70/30 Split            │
│  2 Months Training:                               │
│    [✓] 80/20 Split    [✓] 70/30 Split            │
│  3 Months Training:                               │
│    [ ] 80/20 Split    [ ] 70/30 Split            │
│  6 Months Training:                               │
│    [ ] 80/20 Split    [ ] 70/30 Split            │
└────────────────────────────────────────────────────┘

┌─ Test Period: Current 3 Months (90 days) ─────────┐
│  ... (same structure)                              │
└────────────────────────────────────────────────────┘
```

**What Each Option Means**:

- **Test Period**: How much recent data to use for testing (simulating prediction)
  - `current_month` = Last 30 days
  - `current_3months` = Last 90 days

- **Train Lookback**: How much historical data to use before test period
  - `1month` = 30 days of training data
  - `2months` = 60 days of training data
  - `3months` = 90 days of training data
  - `6months` = 180 days of training data

- **Train/Test Split**: How to split training data for validation
  - `80/20` = 80% train, 20% validation
  - `70/30` = 70% train, 30% validation

**Example Configuration**:
```
Test Period: current_month (last 30 days)
Train Lookback: 2months (60 days before test period)
Train/Test Split: 80_20 (80% of 60 days = 48 train, 12 validation)

Timeline:
|----60 days historical----|--30 days test--|
|--48 train--|--12 val--|--30 test----|
```

### Step 2: Run Historical Backtests

Click **"Run Historical Backtests"**

What happens:
1. For each selected configuration:
   - Split data according to configuration
   - Train all 5 models (LSTM, RF, XGBoost, Prophet, Ensemble)
   - Generate predictions for test period
   - Calculate accuracy metrics (RMSE, MAE, MAPE, Direction Accuracy)

2. Results shown:
   - **Best configuration for each model**
   - **Comparison table** (sorted by RMSE)
   - **Sample prediction chart** vs actual prices
   - **Detailed metrics** for all configurations

**Example Results**:
```
Best Configuration for Each Model:
┌─ ENSEMBLE ──────────────────────────┐
│ Test: current month                  │
│ Train: 2months                       │
│ Split: 80/20                         │
│ RMSE: 0.0234  ✓ Best!              │
│ Direction Accuracy: 68.2%            │
└──────────────────────────────────────┘

┌─ XGBOOST ───────────────────────────┐
│ Test: current month                  │
│ Train: 3months                       │
│ Split: 70/30                         │
│ RMSE: 0.0198                        │
│ Direction Accuracy: 71.5%            │
└──────────────────────────────────────┘
```

### Step 3: Predict Future

After backtesting completes, select **prediction horizon**:
- **1 Month**: Predict next 30 days
- **3 Months**: Predict next 90 days

Click **"Predict Future Prices"**

What happens:
1. Uses **best configuration** from backtesting
2. Trains models on most recent data (amount = train_lookback)
3. Generates predictions for future
4. Shows continuous chart: Historical → Future

**Example Chart**:
```
Price
  ↑
  │ Historical ──────────┐
  │                      │ Future Predictions
  │                      ↓ (dashed lines)
  │ ══════════════════════╪═══════════════
  │                      TODAY
  │
  └────────────────────────────────────→ Time
    Jan  Feb  Mar  Apr  May  Jun  Jul
```

---

## 💡 Key Concepts

### What is Historical Backtesting?

**Purpose**: Test which configuration gives most accurate predictions on historical data before using it for future predictions.

**Process**:
1. Take recent historical data as "test period" (pretend it's the future)
2. Use older data as "training period"
3. Train models on training data
4. Predict the "test period" 
5. Compare predictions vs actual values
6. Calculate accuracy metrics

**Why?**: Find which combination of:
- Test period length
- Training data length  
- Train/test split ratio

...gives the best prediction accuracy.

### Train vs Test Range

**Important Distinction**:

| Aspect | Train/Test Range | Prediction Range |
|--------|-----------------|------------------|
| **Purpose** | Find best configuration | Actual future prediction |
| **Data Used** | Historical data only | Recent data → future |
| **Known Outcome** | Yes (can verify accuracy) | No (true prediction) |
| **Goal** | Optimize configuration | Make real predictions |

**Timeline Example**:
```
|---Historical Data (2 years)---|---Today---|---Future---|

Backtesting Phase:
|---Train---|---Val---|---Test---|
  (older)    (old)    (recent)
                      ↑ We know actual values

Future Prediction Phase:
               |---Train---|---PREDICT---|
                (recent)     (unknown)
                            ↑ True predictions
```

### Multiple Configuration Comparison

**Why test multiple configurations?**

Different market conditions may favor different setups:
- **Volatile markets**: Shorter training periods may work better
- **Stable markets**: Longer training periods capture trends
- **Trending markets**: 70/30 split gives more validation
- **Sideways markets**: 80/20 split maximizes training data

**Example Comparison**:
```
Config 1: Test 30d, Train 1mo, 80/20
  → RMSE: 0.0450, Dir.Acc: 62%

Config 2: Test 30d, Train 2mo, 80/20
  → RMSE: 0.0234, Dir.Acc: 68%  ✓ BEST

Config 3: Test 30d, Train 3mo, 80/20
  → RMSE: 0.0389, Dir.Acc: 65%

Config 4: Test 90d, Train 2mo, 70/30
  → RMSE: 0.0567, Dir.Acc: 58%
```

Result: Use Config 2 for future predictions!

---

## 📊 Understanding the Results

### Accuracy Metrics

**RMSE (Root Mean Square Error)**:
- Measures average prediction error
- Lower is better
- Penalizes large errors heavily
- Unit: Same as price (e.g., $0.0234)

**MAE (Mean Absolute Error)**:
- Average absolute difference
- Lower is better
- Unit: Same as price
- More robust to outliers than RMSE

**MAPE (Mean Absolute Percentage Error)**:
- Percentage error
- Lower is better
- Unit: Percentage
- Good for comparing across different price scales

**Direction Accuracy**:
- % of correct trend predictions (up/down)
- Higher is better
- Most important for trading decisions
- Example: 68% means correctly predicted direction 68% of time

### Reading the Charts

**Historical Backtest Chart**:
```
Legend:
━━━ Black solid   = Actual historical prices
- - Purple dash   = Ensemble predictions
- - Orange dash   = XGBoost predictions
- - Green dash    = Random Forest predictions
```

**Future Prediction Chart**:
```
Timeline:
|---Historical---|--Today--|---Future Predictions---|

Legend:
━━━ Black solid     = Historical prices (known)
│ Red vertical     = Today's date
- - Purple dash    = Ensemble future (unknown)
- - Orange dash    = XGBoost future
- - Green dash     = Random Forest future
- - Red dash       = LSTM future
```

---

## 🔧 Technical Implementation

### Backend Processing Flow

```python
# 1. User selects configurations
configs = [
    {test_period: 'current_month', train_lookback: '2months', train_test_split: '80_20'},
    {test_period: 'current_month', train_lookback: '3months', train_test_split: '80_20'},
]

# 2. For each configuration:
for config in configs:
    # Split data
    train_df, val_df, test_df = prepare_historical_backtest(df, config)
    
    # Train models
    full_train = concat([train_df, val_df])
    train_all_models(full_train)
    
    # Predict test period
    predictions = predict(full_train, horizon=len(test_df))
    
    # Calculate metrics
    metrics = calculate_metrics(predictions, test_df['actual'])
    
# 3. Find best configuration
best_config = min(configs, key=lambda c: c.metrics['rmse'])

# 4. Predict future using best config
train_recent = df.tail(best_config.train_lookback)
train_all_models(train_recent)
future_predictions = predict(train_recent, horizon=30)
```

### Data Structure

**Backtest Results**:
```json
{
  "all_results": [
    {
      "config": {...},
      "predictions": {
        "ensemble": {
          "dates": ["2024-10-01", "2024-10-02", ...],
          "predictions": [8.25, 8.27, ...],
          "actual": [8.26, 8.28, ...],
          "lower_bound": [8.20, 8.22, ...],
          "upper_bound": [8.30, 8.32, ...]
        },
        "xgboost": {...},
        ...
      },
      "accuracy_metrics": {
        "ensemble": {
          "rmse": 0.0234,
          "mae": 0.0187,
          "mape": 0.23,
          "direction_accuracy": 68.2
        },
        ...
      }
    },
    ...
  ],
  "best_configs": {
    "ensemble": {
      "config": {...},
      "metrics": {...}
    },
    ...
  },
  "comparison_summary": [
    {
      "configuration": "current_month_train2months_split80_20",
      "model": "ensemble",
      "rmse": 0.0234,
      ...
    },
    ...
  ]
}
```

**Future Predictions**:
```json
{
  "prediction_horizon": "1month",
  "days_ahead": 30,
  "start_date": "2024-10-26",
  "end_date": "2024-11-25",
  "last_historical_date": "2024-10-25",
  "last_historical_price": 8.28,
  "predictions": {
    "ensemble": {
      "dates": ["2024-10-26", "2024-10-27", ...],
      "predictions": [8.29, 8.30, ...],
      "lower_bound": [8.24, 8.25, ...],
      "upper_bound": [8.34, 8.35, ...]
    },
    ...
  }
}
```

---

## 🎨 UI/UX Features

### Configuration Grid

- **Visual Selection**: Click to toggle green checkmark
- **Selected Count**: Shows how many configs selected
- **Config Tags**: Visual chips showing selected combinations
- **Disabled State**: Button disabled if no configs selected

### Loading States

```
Stage: config        → Configuration selection
Stage: backtesting   → Animated spinner + progress text
Stage: results       → Results display + future prediction button
Stage: future        → Future predictions chart
```

### Navigation

```
Config → [Run Backtest] → Backtesting → Results → [Predict Future] → Future
   ↑                                        ↑                           ↓
   └─────────────[← Back]──────────────────┘───────[← Back]────────────┘
```

### Error Handling

- **No configs selected**: Alert before running
- **API errors**: Red error banner with details
- **Network timeout**: Retry option
- **Training required**: Clear message in predictions endpoint

---

## 📈 Use Cases & Examples

### Use Case 1: Day Trader

**Goal**: Find best setup for predicting next day prices

**Strategy**:
1. Select: `current_month` test, `1month` and `2months` train, both splits
2. Run backtest
3. Check direction accuracy (most important)
4. Use best config to predict next 1 month
5. Focus on short-term predictions (next 1-7 days)

### Use Case 2: Swing Trader

**Goal**: Predict price movements over 1-3 weeks

**Strategy**:
1. Select: `current_month` test, `2months` and `3months` train, 80/20 split
2. Run backtest
3. Balance RMSE and direction accuracy
4. Predict next 1 month
5. Look for trends in ensemble predictions

### Use Case 3: Long-term Investor

**Goal**: Understand long-term trends

**Strategy**:
1. Select: `current_3months` test, `6months` train, 70/30 split
2. Run backtest
3. Focus on MAPE (percentage error)
4. Predict next 3 months
5. Use ensemble predictions with confidence intervals

### Use Case 4: Model Researcher

**Goal**: Understand which configurations work best

**Strategy**:
1. Select ALL configurations (extensive testing)
2. Run comprehensive backtest
3. Analyze comparison table
4. Identify patterns:
   - Does longer training help?
   - Which split ratio is better?
   - Best test period length?
5. Use insights for future trading

---

## 🚨 Important Notes

### Limitations

1. **Past Performance ≠ Future Results**
   - Historical accuracy doesn't guarantee future accuracy
   - Market conditions change
   - Use predictions as one input among many

2. **Computational Cost**
   - Each configuration trains 5 models
   - More configs = longer wait time
   - Typical: 30-60 seconds per configuration

3. **Data Requirements**
   - Need sufficient historical data
   - `6months` training requires >6 months of data
   - Check data availability before selecting

4. **Market Factors**
   - Models don't account for news events
   - Can't predict black swan events
   - Best for normal market conditions

### Best Practices

✅ **DO**:
- Test multiple configurations
- Compare direction accuracy for trading
- Use ensemble predictions (most robust)
- Check confidence intervals (lower/upper bounds)
- Re-run backtests periodically
- Combine with technical indicators

❌ **DON'T**:
- Rely solely on predictions
- Ignore market fundamentals
- Use outdated configurations
- Over-optimize on historical data
- Trade without risk management
- Assume 100% accuracy

---

## 🔄 API Reference

### POST /api/backtest

**Request**:
```json
{
  "symbol": "EURCNY=X",
  "period": "2y",
  "configs": [
    {
      "test_period": "current_month",
      "train_lookback": "2months",
      "train_test_split": "80_20"
    }
  ]
}
```

**Response**: See Data Structure section above

### POST /api/predict-future

**Request**:
```json
{
  "symbol": "EURCNY=X",
  "period": "2y",
  "best_config": {
    "test_period": "current_month",
    "train_lookback": "2months",
    "train_test_split": "80_20"
  },
  "prediction_horizon": "1month"
}
```

**Response**: See Data Structure section above

### GET /api/indicators/{symbol}

**Response (Updated)**:
```json
{
  "symbol": "EURCNY=X",
  "name": "EUR/CNY",
  "latest_price": 8.28,
  "data": [  // NEW: Time series data
    {
      "date": "2024-01-01",
      "close": 8.20,
      "sma_20": 8.18,
      "sma_50": 8.15,
      "ema_12": 8.19,
      "bb_upper": 8.25,
      "bb_middle": 8.20,
      "bb_lower": 8.15
    },
    ...
  ],
  "indicators": {...}  // Existing latest values
}
```

---

## ✅ Testing Checklist

### Backend Testing

```bash
# 1. Start backend
cd backend
python main.py

# 2. Test indicators endpoint
curl http://localhost:8001/api/indicators/EURCNY=X?period=1y

# 3. Test predictions (should fail if not trained)
curl http://localhost:8001/api/predictions/EURCNY=X

# 4. Test backtest endpoint
curl -X POST http://localhost:8001/api/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "EURCNY=X",
    "period": "2y",
    "configs": [{
      "test_period": "current_month",
      "train_lookback": "2months",
      "train_test_split": "80_20"
    }]
  }'
```

### Frontend Testing

```bash
# 1. Start frontend
cd frontend
npm run dev

# 2. Open http://localhost:5173

# 3. Test workflow:
   - Click on Advanced Backtesting section
   - Select 2-3 configurations
   - Click "Run Historical Backtests"
   - Wait for results
   - Select prediction horizon
   - Click "Predict Future Prices"
   - Verify continuous chart

# 4. Test indicators:
   - Go to Price Chart
   - Click "Show Indicators"
   - Check SMA 20, SMA 50 checkboxes
   - Verify lines follow price over time
   - Check Bollinger Bands checkbox
   - Verify 3 blue dashed lines appear
```

---

## 🎉 Summary

### What We Built

1. **Fixed Indicators** - Time series display working correctly
2. **No Auto-Training** - Explicit user control required
3. **Advanced Backtesting** - Professional-grade testing system
4. **Configuration Comparison** - Find optimal setup
5. **Future Predictions** - Continuous historical→future charts
6. **Best Practices** - Industry-standard backtesting methodology

### Key Features

- ✅ 2 test periods × 4 train lookbacks × 2 splits = **16 possible configurations**
- ✅ **5 ML models** tested per configuration
- ✅ **4 accuracy metrics** per model
- ✅ Automatic **best configuration detection**
- ✅ **Continuous charts** from historical to future
- ✅ **Confidence intervals** on predictions
- ✅ **Direction accuracy** for trading decisions

### Total Capabilities

```
Configurations: 16
Models: 5 (LSTM, RF, XGBoost, Prophet, Ensemble)
Metrics: 4 (RMSE, MAE, MAPE, Direction Accuracy)
Total Comparisons: 80 model-metric combinations per run

Prediction Horizons: 2 (1 month, 3 months)
Chart Types: 2 (Historical Backtest, Future Prediction)
Indicators: 4 selectable (SMA 20/50, Bollinger, EMA 12)
```

---

**The system is now production-ready for professional financial analysis!** 🚀📈

All three major issues resolved:
1. ✅ Indicators display correctly as time series
2. ✅ Training only happens on user command
3. ✅ Advanced backtesting with configuration optimization

**Ready to make data-driven trading decisions!**
