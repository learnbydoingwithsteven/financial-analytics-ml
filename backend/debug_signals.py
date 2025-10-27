"""
Debug signals endpoint
"""
import requests
import json

response = requests.get("http://localhost:8000/api/signals/EURCNY=X?period=1y")
data = response.json()

print("Signals Response:")
print(json.dumps(data, indent=2))
