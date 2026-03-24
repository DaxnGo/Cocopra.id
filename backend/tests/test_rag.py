import requests
import json

url = "http://localhost:8000/api/assistant/chat"
payload = {
    "history": [],
    "message": "Apakah saya boleh menyemprot hama kelapa menggunakan pestisida Monokrotofos?"
}

try:
    print("Mengirim pertanyaan ke RAG Engine (Gemini 2)...")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print("\n--- JAWABAN AI ---")
    print(data.get("reply", "Tidak ada balasan"))
    print("------------------")
    print(f"Regulatory Flag (Pelanggaran Terdeteksi): {data.get('regulatory_flag')}")
    
except Exception as e:
    print(f"Error: {e}")
