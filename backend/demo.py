"""
Demo script to test the Financial Analytics system
Run this after starting the backend to verify everything works
"""
import asyncio
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000"

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_health():
    """Test if API is running"""
    print_section("1. Testing API Health")
    try:
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is running!")
            print(f"   Version: {data.get('version')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to API: {str(e)}")
        print("   Make sure backend is running: python main.py")
        return False

def test_assets():
    """Test asset list endpoint"""
    print_section("2. Testing Assets List")
    try:
        response = requests.get(f"{API_BASE}/api/assets")
        if response.status_code == 200:
            data = response.json()
            assets = data.get('assets', [])
            print(f"✅ Found {len(assets)} assets")
            
            # Group by category
            by_category = {}
            for asset in assets:
                cat = asset['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(asset)
            
            for category, items in by_category.items():
                print(f"\n   {category.upper()}: {len(items)} assets")
                for asset in items:
                    print(f"      • {asset['name']} ({asset['symbol']})")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_data_fetch(symbol="EURCNY=X"):
    """Test data fetching for a symbol"""
    print_section(f"3. Testing Data Fetch for {symbol}")
    try:
        response = requests.get(
            f"{API_BASE}/api/data/{symbol}",
            params={"period": "1mo"}
        )
        if response.status_code == 200:
            data = response.json()
            records = data.get('data', [])
            print(f"✅ Fetched {len(records)} days of data")
            print(f"   Symbol: {data.get('name')}")
            print(f"   Period: {data.get('period')}")
            
            if records:
                latest = records[-1]
                print(f"\n   Latest Data ({latest['date']}):")
                print(f"      Open: ${latest['open']:.4f}")
                print(f"      High: ${latest['high']:.4f}")
                print(f"      Low: ${latest['low']:.4f}")
                print(f"      Close: ${latest['close']:.4f}")
                print(f"      Volume: {latest['volume']:,}")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_indicators(symbol="EURCNY=X"):
    """Test technical indicators"""
    print_section(f"4. Testing Technical Indicators for {symbol}")
    try:
        response = requests.get(
            f"{API_BASE}/api/indicators/{symbol}",
            params={"period": "1y"}
        )
        if response.status_code == 200:
            data = response.json()
            indicators = data.get('indicators', {})
            latest_price = data.get('latest_price')
            
            print(f"✅ Calculated technical indicators")
            print(f"   Latest Price: ${latest_price:.4f}")
            
            # Moving Averages
            ma = indicators.get('moving_averages', {})
            print(f"\n   Moving Averages:")
            print(f"      SMA 20: ${ma.get('sma_20', 0):.4f}")
            print(f"      SMA 50: ${ma.get('sma_50', 0):.4f}")
            print(f"      SMA 200: ${ma.get('sma_200', 0):.4f}")
            
            # Momentum
            momentum = indicators.get('momentum', {})
            print(f"\n   Momentum Indicators:")
            print(f"      RSI: {momentum.get('rsi', 0):.2f}")
            print(f"      MACD: {momentum.get('macd', 0):.4f}")
            
            # Volatility
            volatility = indicators.get('volatility', {})
            print(f"\n   Volatility:")
            print(f"      ATR: {volatility.get('atr', 0):.4f}")
            
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_signals(symbol="EURCNY=X"):
    """Test trading signals"""
    print_section(f"5. Testing Trading Signals for {symbol}")
    try:
        response = requests.get(
            f"{API_BASE}/api/signals/{symbol}",
            params={"period": "1y"}
        )
        if response.status_code == 200:
            data = response.json()
            signals = data.get('signals', {})
            overall = signals.get('overall', {})
            
            print(f"✅ Generated trading signals")
            print(f"\n   Overall Recommendation: {overall.get('recommendation')}")
            print(f"   Confidence: {overall.get('confidence')}%")
            print(f"   Buy Signals: {overall.get('buy_signals')}")
            print(f"   Sell Signals: {overall.get('sell_signals')}")
            
            print(f"\n   Individual Signals:")
            for indicator, signal in signals.items():
                if indicator != 'overall':
                    print(f"      {indicator}: {signal.get('signal')} ({signal.get('strength')})")
            
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_model_training(symbol="EURCNY=X"):
    """Test ML model training"""
    print_section(f"6. Testing ML Model Training for {symbol}")
    print("   ⚠️  This may take 30-60 seconds...")
    try:
        response = requests.post(
            f"{API_BASE}/api/train",
            json={"symbol": symbol, "period": "2y"},
            timeout=120
        )
        if response.status_code == 200:
            data = response.json()
            results = data.get('training_results', {})
            
            print(f"\n✅ Models trained successfully!")
            print(f"   Symbol: {data.get('name')}")
            
            for model, result in results.items():
                if result.get('success'):
                    metrics = result.get('metrics', {})
                    print(f"\n   {model.upper()}:")
                    print(f"      RMSE: {metrics.get('rmse', 0):.4f}")
                    print(f"      MAE: {metrics.get('mae', 0):.4f}")
                    print(f"      Direction Accuracy: {metrics.get('direction_accuracy', 0):.1f}%")
                else:
                    print(f"\n   {model.upper()}: ❌ {result.get('error')}")
            
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_predictions(symbol="EURCNY=X"):
    """Test ML predictions"""
    print_section(f"7. Testing ML Predictions for {symbol}")
    try:
        response = requests.get(
            f"{API_BASE}/api/predictions/{symbol}",
            timeout=120
        )
        if response.status_code == 200:
            data = response.json()
            predictions = data.get('predictions', {})
            
            print(f"✅ Generated predictions")
            
            for horizon, models in predictions.items():
                print(f"\n   {horizon.upper()} Predictions:")
                for model, pred_data in models.items():
                    if pred_data.get('success'):
                        preds = pred_data.get('predictions', [])
                        if preds:
                            print(f"      {model}: ${preds[0]:.4f} → ${preds[-1]:.4f} "
                                  f"({((preds[-1] - preds[0]) / preds[0] * 100):+.2f}%)")
            
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "FINANCIAL ANALYTICS DEMO & TEST" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = {}
    
    # Run tests in sequence
    results['health'] = test_health()
    if not results['health']:
        print("\n❌ API is not running. Please start backend first:")
        print("   cd backend")
        print("   python main.py")
        return
    
    results['assets'] = test_assets()
    results['data'] = test_data_fetch()
    results['indicators'] = test_indicators()
    results['signals'] = test_signals()
    results['training'] = test_model_training()
    results['predictions'] = test_predictions()
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test.capitalize():<15} {status}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n   🎉 All tests passed! System is fully operational.")
        print("\n   Next steps:")
        print("      1. Start frontend: cd frontend && npm run dev")
        print("      2. Open browser: http://localhost:5173")
        print("      3. Explore the dashboard!")
    else:
        print("\n   ⚠️  Some tests failed. Check the errors above.")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
