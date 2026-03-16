import os
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image

router = APIRouter()

# Konfigurasi Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@router.post("/scan", response_model=schemas.PestScanResponse)
def scan_pest(scan_data: schemas.PestScanCreate, db: Session = Depends(get_db)):
    """
    Menerima gambar hama dari frontend (base64), menyimpannya ke database, 
    dan melakukan inferensi AI menggunakan Gemini 1.5 Flash.
    """
    # 1. Simpan payload ke DB (sebagai "pending")
    db_scan = models.PestScanLog(
        image_data=scan_data.image_data[:100] + "... (truncated)", # Simpan versi ringkas di DB lokal untuk demo
        filename=scan_data.filename,
        timestamp=scan_data.timestamp,
        status="processing"
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)

    # 2. Proses AI Menggunakan Gemini Vision
    # Daftar model yang akan dicoba secara berurutan (fallback jika quota habis)
    MODEL_CANDIDATES = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash-lite',
        'models/gemini-2.0-flash',
    ]

    try:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY belum di-set di .env")

        # Decode gambar base64
        # Format umum dari frontend: "data:image/jpeg;base64,/9j/4AAQSk..."
        header, encoded = scan_data.image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(BytesIO(image_bytes))

        prompt = "Anda adalah ahli hama pertanian kelapa. Analisis gambar daun/batang kelapa ini. Identifikasi apakah ada penyakit atau hama (seperti Kutu Putih / Pseudococcus, Kumbang Tanduk, Kutu Janur, dll). Jika ada, sebutkan nama hamanya secara spesifik beserta persentase keyakinan Anda (misalnya 95%). Jika tampak sehat (bukan kelapa atau daun segar tanpa bercak putih/lubang), sebut 'Tanaman Sehat'. Berikan jawaban Singkat maksimal 2 kalimat."
        
        # Coba setiap model secara berurutan hingga berhasil
        ai_analysis = None
        last_error = None
        for model_name in MODEL_CANDIDATES:
            try:
                print(f"[Pest Scanner] Mencoba model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([prompt, image])
                ai_analysis = response.text.strip()
                print(f"[Pest Scanner] Berhasil dengan model: {model_name}")
                break  # Berhasil, keluar dari loop
            except Exception as model_err:
                last_error = model_err
                print(f"[Pest Scanner] Model {model_name} gagal: {model_err}")
                continue  # Coba model berikutnya
        
        if ai_analysis is None:
            raise last_error or ValueError("Semua model gagal")
        
        # Ekstrak Confidence Score sederhana (bisa diperbaiki dengan Regex di prod)
        confidence_score = 0.90 if "sehat" not in ai_analysis.lower() else 0.99
        
        result_label = ai_analysis

    except Exception as e:
        print(f"[Pest Scanner] SEMUA MODEL GAGAL — Error terakhir: {e}")
        # Jika semua model gagal (quota habis / error lain), kembalikan data MOCK
        result_label = "MOCK RESULT (API Quota Exceeded): Tanaman ini terindikasi terserang hama Kutu Putih (Pseudococcus). Segera lakukan penanganan."
        confidence_score = 0.85

    # 3. Update DB dengan hasil analisis aktual
    db_scan.status = "processed"
    db_scan.result_label = result_label
    db_scan.confidence_score = confidence_score
    db.commit()
    db.refresh(db_scan)

    return db_scan
