"""
Quick API test
"""
import requests
import json

API_BASE = "http://localhost:8000"

print("=" * 60)
print("Testing Financial Analytics API")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get(f"{API_BASE}/")
    if response.status_code == 200:
        print("✅ API is running!")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Status code: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get assets
print("\n2. Testing /api/assets...")
try:
    response = requests.get(f"{API_BASE}/api/assets")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['assets'])} assets")
        print(f"   First 3: {[a['symbol'] for a in data['assets'][:3]]}")
    else:
        print(f"❌ Status code: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Get data for EUR/CNY
print("\n3. Testing /api/data/EURCNY=X...")
try:
    response = requests.get(f"{API_BASE}/api/data/EURCNY=X?period=1mo")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Fetched {data['records']} days of data")
        if data['data']:
            latest = data['data'][-1]
            print(f"   Latest close: ${latest['close']:.4f}")
    else:
        print(f"❌ Status code: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Get indicators
print("\n4. Testing /api/indicators/EURCNY=X...")
try:
    response = requests.get(f"{API_BASE}/api/indicators/EURCNY=X?period=6mo")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Got indicators!")
        print(f"   Price: ${data['latest_price']:.4f}")
        ma = data['indicators']['moving_averages']
        print(f"   SMA 20: ${ma.get('sma_20', 0):.4f}")
        print(f"   RSI: {data['indicators']['momentum'].get('rsi', 'N/A')}")
    else:
        print(f"❌ Status code: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Get signals
print("\n5. Testing /api/signals/EURCNY=X...")
try:
    response = requests.get(f"{API_BASE}/api/signals/EURCNY=X?period=6mo")
    if response.status_code == 200:
        data = response.json()
        signals = data['signals']
        if 'overall' in signals:
            overall = signals['overall']
            print(f"✅ Got signals!")
            print(f"   Recommendation: {overall.get('recommendation')}")
            print(f"   Confidence: {overall.get('confidence')}%")
        else:
            print(f"⚠️  Signals generated but no overall recommendation")
    else:
        print(f"❌ Status code: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
