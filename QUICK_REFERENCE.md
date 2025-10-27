# Quick Reference Card

## ⚡ One-Line Start

```bash
# Windows
start.bat

# Mac/Linux
./start.sh
```

---

## 📋 Essential Commands

### Backend
```bash
cd backend
pip install -r requirements.txt    # Install
python test_installation.py        # Test setup
python main.py                      # Start server
python demo.py                      # Run tests
```

### Frontend
```bash
cd frontend
npm install          # Install
npm run dev          # Start dev server
npm run build        # Build for production
```

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:5173 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 📊 Assets Available

| Category | Symbol | Name |
|----------|--------|------|
| Forex | EURCNY=X | EUR/CNY |
| Commodity | GC=F | Gold |
| US Bond | TLT | 20+ Year Treasury |
| US Bond | IEF | 7-10 Year Treasury |
| CN Bond | CBON | China Bond ETF |
| US Index | ^GSPC | S&P 500 |
| US Index | ^DJI | Dow Jones |
| US Index | ^IXIC | NASDAQ |
| CN Index | 000001.SS | Shanghai |
| CN Index | 399001.SZ | Shenzhen |
| CN Index | ^HSI | Hang Seng |

---

## 📈 Technical Indicators

### Trend
- SMA 20, 50, 200
- EMA 12, 26
- MACD

### Momentum
- RSI (14)
- Stochastic K & D
- CCI (20)

### Volatility
- Bollinger Bands
- ATR (14)

### Volume
- OBV

---

## 🤖 ML Models

1. **LSTM** - Neural network (30-60s training)
2. **Random Forest** - Tree ensemble (5-10s)
3. **XGBoost** - Gradient boosting (10-15s)
4. **Prophet** - Time series (15-20s)
5. **ARIMA** - Statistical (5-10s)
6. **Ensemble** - Combined (all above)

---

## 📅 Time Horizons

| Code | Period | Days |
|------|--------|------|
| 1m | 1 month | 21 |
| 2m | 2 months | 42 |
| 3m | 3 months | 63 |
| 6m | 6 months | 126 |

---

## 🎯 API Endpoints

```bash
GET  /api/assets                    # List assets
GET  /api/data/{symbol}            # Historical data
GET  /api/indicators/{symbol}      # Technical indicators
GET  /api/signals/{symbol}         # Buy/sell signals
POST /api/train                    # Train ML models
GET  /api/predictions/{symbol}     # ML predictions
GET  /api/models/performance/{symbol}  # Model comparison
GET  /api/latest/{symbol}          # Latest price
```

---

## 🔧 Quick Fixes

### Backend Won't Start
```bash
pip install -r requirements.txt
python main.py
```

### Frontend Won't Start
```bash
rm -rf node_modules
npm install
npm run dev
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

### API Not Responding
```bash
# Check if backend is running
curl http://localhost:8000/

# Restart backend
cd backend
python main.py
```

---

## 📊 Signal Interpretation

| Signal | Meaning | Action |
|--------|---------|--------|
| STRONG BUY | >60% buy signals | Consider buying |
| BUY | 50-60% buy signals | Moderate buy |
| HOLD | Mixed signals | Wait |
| SELL | 50-60% sell signals | Moderate sell |
| STRONG SELL | >60% sell signals | Consider selling |

---

## 📈 Indicator Thresholds

| Indicator | Buy Zone | Sell Zone |
|-----------|----------|-----------|
| RSI | < 30 | > 70 |
| Stochastic | < 20 | > 80 |
| Price vs SMA | Above | Below |
| MACD | > Signal | < Signal |
| Bollinger | Near lower | Near upper |

---

## 💻 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Refresh | F5 |
| Console | F12 |
| Hard Refresh | Ctrl+Shift+R |

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| README.md | Project overview |
| INSTALLATION.md | Setup guide |
| FEATURES.md | Feature details |
| API_DOCUMENTATION.md | API reference |
| TROUBLESHOOTING.md | Problem solving |
| FINAL_SUMMARY.md | Project completion |

---

## 🔍 Testing Commands

```bash
# Test installation
cd backend
python test_installation.py

# Test API
python demo.py

# Test single endpoint
curl http://localhost:8000/api/assets
```

---

## 📦 Dependencies

### Backend
- Python 3.9+
- FastAPI, pandas, numpy
- yfinance, pandas-ta
- scikit-learn, xgboost
- tensorflow, prophet

### Frontend
- Node.js 18+
- React 18
- Vite, TailwindCSS
- Recharts, Axios

---

## 🎨 Color Codes (Signals)

| Color | Signal | CSS Class |
|-------|--------|-----------|
| 🟢 Green | Buy | signal-buy |
| 🔴 Red | Sell | signal-sell |
| ⚪ Gray | Neutral | signal-neutral |

---

## 📊 Performance Metrics

| Metric | Formula | Best Value |
|--------|---------|------------|
| RMSE | √(Σ(y-ŷ)²/n) | Lower |
| MAE | Σ\|y-ŷ\|/n | Lower |
| MAPE | Σ\|y-ŷ\|/y×100/n | Lower |
| Direction | % correct trends | Higher |

---

## 🚀 Deployment

### Docker
```bash
docker-compose up
```

### Production
```bash
# Backend
cd backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Frontend
cd frontend
npm run build
# Serve dist/ folder
```

---

## 💡 Pro Tips

1. ✅ Train models with 2y data
2. ✅ Use ensemble for best results
3. ✅ Check confidence scores
4. ✅ Compare multiple indicators
5. ✅ Monitor direction accuracy
6. ✅ Cache trained models
7. ✅ Start with shorter periods
8. ✅ Combine technical + ML signals

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Port in use | Kill process or change port |
| No data | Check symbol on Yahoo Finance |
| CORS error | Ensure backend is running |
| White screen | Check browser console (F12) |

---

## 📞 Help Resources

1. TROUBLESHOOTING.md
2. API docs: http://localhost:8000/docs
3. Browser console (F12)
4. Terminal logs
5. Demo script: `python demo.py`

---

## ✅ Quick Checklist

Before starting:
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Internet connection
- [ ] Ports 8000 & 5173 available

After installation:
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Dashboard loads in browser

---

## 🎯 First Steps

1. Install (5 min)
2. Start servers (1 min)
3. Open dashboard
4. Select EUR/CNY
5. View indicators
6. Check signals
7. Train models (60s)
8. View predictions

---

**Print this card for quick reference! 📄**

**Dashboard:** http://localhost:5173  
**API:** http://localhost:8000  
**Docs:** http://localhost:8000/docs
