"""
Test script to verify backend installation
Run this to check if all dependencies are installed correctly
"""
import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    print("-" * 50)
    
    packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
        'yfinance': 'yfinance',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'pandas_ta': 'pandas-ta',
    }
    
    optional_packages = {
        'tensorflow': 'TensorFlow (for LSTM)',
        'xgboost': 'XGBoost',
        'prophet': 'Prophet',
    }
    
    success = True
    
    # Test required packages
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name:<20} - OK")
        except ImportError as e:
            print(f"❌ {name:<20} - MISSING")
            print(f"   Install with: pip install {module}")
            success = False
    
    print("\nOptional packages (for ML models):")
    print("-" * 50)
    
    # Test optional packages
    for module, name in optional_packages.items():
        try:
            __import__(module)
            print(f"✅ {name:<30} - OK")
        except ImportError:
            print(f"⚠️  {name:<30} - MISSING (optional)")
    
    return success

def test_data_fetch():
    """Test if we can fetch data from Yahoo Finance"""
    print("\n" + "=" * 50)
    print("Testing data fetch from Yahoo Finance...")
    print("-" * 50)
    
    try:
        import yfinance as yf
        
        # Try to fetch sample data
        ticker = yf.Ticker("GC=F")  # Gold futures
        data = ticker.history(period="5d")
        
        if not data.empty:
            print("✅ Data fetch successful!")
            print(f"   Retrieved {len(data)} days of data for Gold")
            print(f"   Latest price: ${data['Close'].iloc[-1]:.2f}")
            return True
        else:
            print("❌ Data fetch failed - no data returned")
            return False
            
    except Exception as e:
        print(f"❌ Data fetch failed: {str(e)}")
        return False

def test_indicators():
    """Test if technical indicators can be calculated"""
    print("\n" + "=" * 50)
    print("Testing technical indicators calculation...")
    print("-" * 50)
    
    try:
        import pandas as pd
        import numpy as np
        import pandas_ta as ta
        
        # Create sample data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        prices = 100 + np.cumsum(np.random.randn(100) * 2)
        df = pd.DataFrame({
            'close': prices,
            'high': prices + np.abs(np.random.randn(100)),
            'low': prices - np.abs(np.random.randn(100)),
            'volume': np.random.randint(1000000, 10000000, 100)
        }, index=dates)
        
        # Calculate some indicators
        sma = ta.sma(df['close'], length=20)
        rsi = ta.rsi(df['close'], length=14)
        
        if sma is not None and rsi is not None:
            print("✅ Technical indicators working!")
            print(f"   SMA(20): {sma.iloc[-1]:.2f}")
            print(f"   RSI(14): {rsi.iloc[-1]:.2f}")
            return True
        else:
            print("❌ Indicator calculation failed")
            return False
            
    except Exception as e:
        print(f"❌ Indicator test failed: {str(e)}")
        return False

def test_ml_models():
    """Test if ML models can be initialized"""
    print("\n" + "=" * 50)
    print("Testing ML model availability...")
    print("-" * 50)
    
    models_status = {}
    
    # Test scikit-learn models
    try:
        from sklearn.ensemble import RandomForestRegressor
        RandomForestRegressor(n_estimators=10)
        models_status['Random Forest'] = True
        print("✅ Random Forest - OK")
    except Exception as e:
        models_status['Random Forest'] = False
        print(f"❌ Random Forest - Failed: {str(e)}")
    
    # Test XGBoost
    try:
        import xgboost as xgb
        xgb.XGBRegressor(n_estimators=10)
        models_status['XGBoost'] = True
        print("✅ XGBoost - OK")
    except Exception as e:
        models_status['XGBoost'] = False
        print(f"⚠️  XGBoost - Not available (optional)")
    
    # Test Prophet
    try:
        from prophet import Prophet
        Prophet()
        models_status['Prophet'] = True
        print("✅ Prophet - OK")
    except Exception as e:
        models_status['Prophet'] = False
        print(f"⚠️  Prophet - Not available (optional)")
    
    # Test TensorFlow/LSTM
    try:
        import tensorflow as tf
        from tensorflow import keras
        models_status['LSTM'] = True
        print("✅ TensorFlow/LSTM - OK")
    except Exception as e:
        models_status['LSTM'] = False
        print(f"⚠️  TensorFlow/LSTM - Not available (optional)")
    
    return any(models_status.values())

def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("FINANCIAL ANALYTICS BACKEND - INSTALLATION TEST")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print("=" * 50)
    
    results = {
        'imports': test_imports(),
        'data_fetch': test_data_fetch(),
        'indicators': test_indicators(),
        'ml_models': test_ml_models(),
    }
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test.replace('_', ' ').title():<20} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Backend is ready to use.")
        print("Run 'python main.py' to start the server.")
    else:
        print("⚠️  Some tests failed. Please install missing packages.")
        print("Run: pip install -r requirements.txt")
    print("=" * 50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
