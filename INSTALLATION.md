# Financial Analytics Dashboard - Installation Guide

## 🚀 Quick Start (5 Minutes)

### Option 1: Automated Start (Recommended)

#### Windows
```bash
# Double-click start.bat or run:
start.bat
```

#### Mac/Linux
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

#### Terminal 1 - Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📋 Prerequisites

### Required Software
- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)

### Verify Installation
```bash
python --version    # Should show 3.9+
node --version      # Should show 18+
npm --version       # Should show 9+
```

## 🔧 Detailed Installation

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

#### Backend Dependencies
The following will be installed:
- **FastAPI** - Web framework
- **yfinance** - Yahoo Finance data
- **pandas, numpy** - Data processing
- **pandas-ta** - Technical indicators
- **scikit-learn** - ML models
- **xgboost** - Gradient boosting
- **prophet** - Time series forecasting
- **tensorflow** - Deep learning (LSTM)

### Step 2: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

#### Frontend Dependencies
The following will be installed:
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Charts
- **React Query** - Data fetching
- **Axios** - HTTP client

### Step 3: Start Services

#### Start Backend (Terminal 1)
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 4: Access Dashboard

Open your browser and go to: **http://localhost:5173**

## 🐛 Troubleshooting

### Backend Issues

#### Issue: Python not found
**Solution**: Install Python 3.9+ from python.org

#### Issue: pip not found
**Solution**: 
```bash
python -m ensurepip --upgrade
```

#### Issue: TensorFlow installation fails
**Windows/Linux**:
```bash
pip install tensorflow==2.15.0
```

**Mac (Apple Silicon)**:
```bash
pip install tensorflow-macos tensorflow-metal
```

#### Issue: Port 8000 in use
**Solution**: Kill the process or change port in `config.py`
```bash
# Find process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Find process (Mac/Linux)
lsof -i :8000
kill -9 <PID>
```

### Frontend Issues

#### Issue: npm not found
**Solution**: Install Node.js from nodejs.org

#### Issue: npm install fails
**Solution**: Clear cache and retry
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### Issue: Port 5173 in use
**Solution**: Vite will automatically use next available port

#### Issue: API connection failed
**Solution**: Ensure backend is running on port 8000
```bash
curl http://localhost:8000/
```

### Data Issues

#### Issue: No data for symbol
**Solution**: Symbol might not be available or misspelled
- Check symbol on Yahoo Finance first
- Try alternative symbols

#### Issue: Rate limiting
**Solution**: Yahoo Finance rarely limits, but if it happens:
- Wait a few minutes
- Use longer cache duration

## ✅ Verification Steps

### 1. Check Backend Health
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Financial Analytics API",
  "version": "1.0.0"
}
```

### 2. Check API Documentation
Open: **http://localhost:8000/docs**

You should see interactive API documentation.

### 3. Test Data Fetch
```bash
curl http://localhost:8000/api/assets
```

Should return list of all tracked assets.

### 4. Check Frontend
Open: **http://localhost:5173**

You should see the dashboard with:
- Asset selector
- Price chart
- Technical indicators
- Signals summary

## 🎯 First Time Usage

### 1. Select an Asset
- Click on asset selector dropdown
- Choose "EUR/CNY" or any other asset

### 2. View Technical Indicators
- Indicators will load automatically
- Check buy/sell signals

### 3. Generate ML Predictions
- ML models will train automatically (first time takes ~60 seconds)
- View predictions for different horizons
- Compare model performance

## 🔐 Security Notes

### Production Deployment
If deploying to production:

1. **Change default ports**
2. **Add authentication**
3. **Use HTTPS**
4. **Set up firewall rules**
5. **Use environment variables for secrets**

### Data Privacy
- All data is fetched from public Yahoo Finance
- No personal data is stored
- No authentication required for local use

## 📊 Performance Tips

### Backend Optimization
- Use caching for frequently accessed data
- Run model training as background tasks
- Consider database for historical predictions

### Frontend Optimization
- Build for production: `npm run build`
- Enable lazy loading for components
- Use CDN for static assets

## 🆘 Getting Help

### Check Logs

**Backend logs**: Look in terminal running `main.py`

**Frontend logs**: Check browser console (F12)

### Common Solutions

1. **Restart both servers**
2. **Clear browser cache**
3. **Update dependencies**
4. **Check network connectivity**

### Still Having Issues?

1. Check if ports 8000 and 5173 are available
2. Verify Python and Node.js versions
3. Make sure all dependencies installed
4. Check firewall settings

## 📈 Next Steps

After successful installation:

1. ✅ Explore different assets
2. ✅ Analyze technical indicators
3. ✅ Generate ML predictions
4. ✅ Compare model performance
5. ✅ Experiment with different time periods

## 🎓 Learning Path

### Beginner
1. Start with price charts
2. Learn basic indicators (SMA, RSI)
3. Understand buy/sell signals

### Intermediate
1. Compare multiple indicators
2. Analyze model predictions
3. Study model performance

### Advanced
1. Modify technical indicators
2. Add new ML models
3. Customize the dashboard

## 🌟 Success!

If you can see the dashboard with live data and ML predictions, you're all set! 🎉

**Dashboard URL**: http://localhost:5173
**API Docs**: http://localhost:8000/docs

Happy Trading! 📈📊💹
