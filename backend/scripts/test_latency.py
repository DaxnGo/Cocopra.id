import time
import requests

start = time.time()
try:
    r = requests.get("http://127.0.0.1:8000/api/health")
    print(f"Status: {r.status_code}")
except Exception as e:
    print(f"Error: {e}")
end = time.time()
print(f"Time (127.0.0.1): {(end-start)*1000:.2f} ms")
