import requests

try:
    response = requests.post(
        "http://localhost:8000/api/assistant/chat",
        headers={"Content-Type": "application/json"},
        json={"history": [], "message": "tes"}
    )
    print(response.status_code)
    print(response.text)
except Exception as e:
    print("Error:", e)
