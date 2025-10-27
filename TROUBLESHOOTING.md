# Troubleshooting Guide

## Quick Diagnostics

Run these commands to check your setup:

```bash
# Check Python version (should be 3.9+)
python --version

# Check Node.js version (should be 18+)
node --version

# Test backend installation
cd backend
python test_installation.py

# Test backend API (after starting server)
python demo.py
```

---

## Backend Issues

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Cause:** Python dependencies not installed

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

**If still failing:**
```bash
# Make sure you're using the correct Python
which python  # Mac/Linux
where python  # Windows

# Try with python3
python3 -m pip install -r requirements.txt
```

---

### Issue: `ImportError: cannot import name 'Prophet' from 'prophet'`

**Cause:** Prophet not installed or incompatible version

**Solution:**
```bash
pip install prophet==1.1.5

# On Mac with Apple Silicon:
conda install -c conda-forge prophet

# If conda not available:
pip install pystan==2.19.1.1
pip install prophet==1.1.5
```

---

### Issue: `No module named 'tensorflow'` or TensorFlow errors

**Cause:** TensorFlow not installed or incompatible

**Solution:**

**Windows/Linux:**
```bash
pip install tensorflow==2.15.0
```

**Mac (Intel):**
```bash
pip install tensorflow==2.15.0
```

**Mac (Apple Silicon M1/M2):**
```bash
pip install tensorflow-macos==2.15.0
pip install tensorflow-metal==1.1.0
```

**If TensorFlow keeps failing:**
The dashboard will work without LSTM model. Other models (Random Forest, XGBoost, Prophet) will still function.

---

### Issue: `Port 8000 already in use`

**Cause:** Another process is using port 8000

**Solution:**

**Find and kill the process:**

Windows:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Mac/Linux:
```bash
lsof -i :8000
kill -9 <PID>
```

**Or change the port:**
Edit `backend/config.py`:
```python
API_PORT = 8001  # Change to any available port
```

Then update frontend proxy in `frontend/vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8001',  // Match new port
    ...
  }
}
```

---

### Issue: `yfinance` not fetching data / Empty DataFrame

**Cause:** Network issues, symbol doesn't exist, or Yahoo Finance rate limit

**Solution:**

1. **Check internet connection**
```bash
ping yahoo.com
```

2. **Verify symbol exists:**
Visit `https://finance.yahoo.com/quote/SYMBOL` and check if valid

3. **Try different period:**
```python
import yfinance as yf
ticker = yf.Ticker("EURCNY=X")
data = ticker.history(period="1mo")  # Start with shorter period
print(data)
```

4. **Wait and retry:**
If rate limited, wait 5-10 minutes

5. **Check yfinance version:**
```bash
pip install --upgrade yfinance
```

---

### Issue: `pandas_ta` indicator calculation fails

**Cause:** Insufficient data or NaN values

**Solution:**

1. **Use longer time period:**
```python
# Need at least 200 days for SMA 200
df = data_fetcher.get_historical_data(symbol, period="1y")
```

2. **Check for NaN values:**
```python
import pandas as pd
print(df.isnull().sum())
df = df.dropna()
```

---

### Issue: Model training is very slow

**Cause:** Normal for first run, especially LSTM

**Expected Times:**
- Random Forest: 5-10 seconds
- XGBoost: 10-15 seconds
- Prophet: 15-20 seconds
- LSTM: 30-60 seconds

**Solutions:**
1. **Reduce data size:**
```python
# In config.py
DATA_LOOKBACK_DAYS = 365  # Instead of 730
```

2. **Reduce LSTM epochs:**
```python
# In ml_models/lstm_model.py
self.epochs = 25  # Instead of 50
```

3. **Skip TensorFlow:**
If LSTM is too slow, the system works fine with other 5 models

---

### Issue: `CORS policy` error in console

**Cause:** Frontend can't connect to backend

**Solution:**

1. **Make sure backend is running:**
```bash
cd backend
python main.py
# Should see: "Uvicorn running on http://0.0.0.0:8000"
```

2. **Check CORS settings in `backend/config.py`:**
```python
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Add your origin if different
]
```

3. **Restart both servers**

---

## Frontend Issues

### Issue: `npm install` fails

**Cause:** Various dependency conflicts

**Solution:**

1. **Clear cache and retry:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

2. **Use specific Node version:**
```bash
# Install nvm first
nvm install 18
nvm use 18
npm install
```

3. **Skip optional dependencies:**
```bash
npm install --no-optional
```

---

### Issue: `npm run dev` fails to start

**Cause:** Port conflict or missing dependencies

**Solution:**

1. **Check if dependencies installed:**
```bash
ls node_modules/  # Should see many folders
npm install  # If not
```

2. **Port 5173 in use:**
Vite will automatically try next available port (5174, 5175, etc.)

3. **Check for errors:**
Look at error message carefully - usually indicates missing package

---

### Issue: White screen / React errors in console

**Cause:** JavaScript errors, API connection issues

**Solution:**

1. **Open browser console (F12)** and check errors

2. **Check API connection:**
```javascript
// In browser console
fetch('http://localhost:8000/')
  .then(r => r.json())
  .then(d => console.log(d))
```

3. **Hard refresh:**
`Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

4. **Clear browser cache**

---

### Issue: Charts not displaying

**Cause:** Data not loaded, Recharts issue

**Solution:**

1. **Check network tab (F12):**
Look for failed API requests

2. **Verify data format:**
```javascript
// In browser console
fetch('http://localhost:8000/api/data/EURCNY=X?period=1mo')
  .then(r => r.json())
  .then(d => console.log(d.data))
```

3. **Check for console errors**

---

### Issue: "Failed to fetch" errors

**Cause:** Backend not running or wrong URL

**Solution:**

1. **Verify backend is running:**
Open `http://localhost:8000/` in browser

2. **Check API_BASE_URL in `frontend/src/services/api.js`:**
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

3. **Check proxy in `frontend/vite.config.js`**

---

## Data Issues

### Issue: No data for specific symbol

**Cause:** Symbol not available on Yahoo Finance

**Solution:**

1. **Verify symbol:**
Visit `https://finance.yahoo.com/quote/SYMBOL`

2. **Try alternative symbols:**
- EUR/CNY: Try "CNY=X" or "EURCNY=X"
- Gold: Try "GC=F" or "GOLD"
- Check Yahoo Finance for correct symbol

3. **Update `backend/config.py`** with correct symbol

---

### Issue: Predictions are not realistic

**Cause:** Normal ML uncertainty, insufficient training data

**Solution:**

1. **Train with more data:**
```python
# Use 2-5 years for better results
data = get_historical_data(symbol, period="5y")
```

2. **Check model performance:**
Look at RMSE, MAE, and direction accuracy

3. **Use ensemble model:**
Ensemble combines all models and is most reliable

4. **Remember:** ML predictions are estimates, not guarantees

---

### Issue: Indicators showing "N/A"

**Cause:** Insufficient historical data

**Solution:**

1. **Use longer period:**
Change from "1mo" to "6mo" or "1y"

2. **Check data availability:**
Some assets have limited history

3. **Wait for more data:**
New assets need time to accumulate history

---

## Performance Issues

### Issue: Dashboard is slow

**Solutions:**

1. **Reduce data fetching:**
- Use shorter time periods
- Cache results client-side

2. **Optimize React:**
```bash
# Build for production
cd frontend
npm run build
```

3. **Increase cache duration in backend**

---

### Issue: High memory usage

**Cause:** Multiple models, large datasets

**Solutions:**

1. **Train models one at a time**
2. **Reduce data lookback period**
3. **Use fewer models (disable LSTM if needed)**
4. **Increase system RAM**

---

## Docker Issues

### Issue: Docker container won't start

**Solution:**

1. **Check Docker is running:**
```bash
docker --version
docker ps
```

2. **Rebuild images:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

3. **Check logs:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

---

## Platform-Specific Issues

### Windows

**Issue:** `'python' is not recognized`
```cmd
# Use full path
C:\Python39\python.exe main.py

# Or add Python to PATH
```

**Issue:** Port binding on Windows
```cmd
# Run as administrator
# Or use different ports
```

### Mac

**Issue:** Apple Silicon compatibility
```bash
# Use Rosetta for incompatible packages
arch -x86_64 pip install package_name

# Or use Anaconda
conda install package_name
```

### Linux

**Issue:** Permission denied
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
```

---

## Common Error Messages

### `Connection refused` or `Connection reset`

**Meaning:** Backend server is not running or wrong port

**Fix:** Start backend server: `python main.py`

---

### `404 Not Found`

**Meaning:** Endpoint doesn't exist or symbol not found

**Fix:** Check API documentation for correct endpoints

---

### `500 Internal Server Error`

**Meaning:** Backend error (data fetch failed, calculation error)

**Fix:** Check backend terminal for error logs

---

### `TypeError: Cannot read property 'map' of undefined`

**Meaning:** Frontend trying to access data that doesn't exist

**Fix:** Check API responses, add null checks in code

---

## Still Having Issues?

### Debugging Steps:

1. **Check versions:**
```bash
python --version  # Should be 3.9+
node --version    # Should be 18+
npm --version     # Should be 9+
```

2. **Check all dependencies installed:**
```bash
cd backend && python test_installation.py
cd frontend && npm list
```

3. **Check processes running:**
```bash
# Backend should be on 8000
# Frontend should be on 5173
```

4. **Review logs carefully:**
- Backend: Terminal running `main.py`
- Frontend: Terminal running `npm run dev`
- Browser: Console (F12)

5. **Try clean reinstall:**
```bash
# Backend
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Getting Help

If you're still stuck:

1. **Check error message carefully** - Often tells you exactly what's wrong
2. **Search error online** - Someone likely had the same issue
3. **Review documentation** - README.md, INSTALLATION.md, API_DOCUMENTATION.md
4. **Check GitHub issues** - If using from repo
5. **Ask for help** - Provide full error message and steps to reproduce

---

## Prevention Tips

1. ✅ Use virtual environment for Python
2. ✅ Keep dependencies updated
3. ✅ Use stable versions (avoid "latest")
4. ✅ Test installation with `test_installation.py` and `demo.py`
5. ✅ Read error messages carefully
6. ✅ Check logs in all terminals
7. ✅ Start with simple examples before complex usage
8. ✅ Back up working configurations

---

**Remember:** Most issues are environment-related and can be fixed with proper setup!
