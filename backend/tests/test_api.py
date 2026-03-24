import requests
import json
from datetime import datetime

url = "http://localhost:8000/api/harga/"
payload = {
    "harga": 8500,
    "lokasi": "Desa Airmadidi",
    "pembeli": "Tengkulak A",
    "timestamp": datetime.utcnow().isoformat()
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body json: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
