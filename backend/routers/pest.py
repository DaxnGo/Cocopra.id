import base64
import os
from io import BytesIO

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from google import genai
from PIL import Image
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

load_dotenv()

router = APIRouter()

# Konfigurasi Gemini (SDK google-genai)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
_gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Daftar model yang dicoba berurutan (fallback jika kuota/model bermasalah)
MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]

PROMPT = (
    "Anda adalah ahli hama pertanian kelapa. Analisis gambar daun/batang kelapa ini. "
    "Identifikasi apakah ada penyakit atau hama (seperti Kutu Putih / Pseudococcus, "
    "Kumbang Tanduk, Kutu Janur, dll). Jika ada, sebutkan nama hamanya secara spesifik "
    "beserta persentase keyakinan Anda (misalnya 95%). Jika tampak sehat (bukan kelapa "
    "atau daun segar tanpa bercak putih/lubang), sebut 'Tanaman Sehat'. "
    "Berikan jawaban singkat maksimal 2 kalimat."
)


@router.post("/scan", response_model=schemas.PestScanResponse)
def scan_pest(scan_data: schemas.PestScanCreate, db: Session = Depends(get_db)):
    """
    Menerima gambar hama dari frontend (base64), menyimpannya ke database,
    dan melakukan inferensi AI menggunakan Gemini Vision.

    Jika AI tidak tersedia, endpoint mengembalikan error yang jelas —
    tidak ada hasil analisis palsu.
    """
    if _gemini_client is None:
        raise HTTPException(
            status_code=503,
            detail="Layanan analisis AI belum dikonfigurasi (GEMINI_API_KEY belum di-set di server).",
        )

    # 1. Simpan payload ke DB (sebagai "processing")
    db_scan = models.PestScanLog(
        image_data=scan_data.image_data[:100] + "... (truncated)",  # ringkas untuk DB lokal demo
        filename=scan_data.filename,
        timestamp=scan_data.timestamp,
        status="processing"
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)

    # 2. Decode gambar base64 (format: "data:image/jpeg;base64,...")
    try:
        _, encoded = scan_data.image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(BytesIO(image_bytes))
    except Exception as e:
        db_scan.status = "failed"
        db_scan.result_label = "Format gambar tidak valid"
        db.commit()
        raise HTTPException(
            status_code=400,
            detail="Format gambar tidak valid — kirim data URL base64 (data:image/...).",
        ) from e

    # 3. Inferensi AI dengan fallback antar-model
    ai_analysis = None
    last_error = None
    for model_name in MODEL_CANDIDATES:
        try:
            print(f"[Pest Scanner] Mencoba model: {model_name}")
            response = _gemini_client.models.generate_content(
                model=model_name,
                contents=[PROMPT, image],
            )
            ai_analysis = (response.text or "").strip() or None
            if ai_analysis:
                print(f"[Pest Scanner] Berhasil dengan model: {model_name}")
                break
        except Exception as model_err:
            last_error = model_err
            print(f"[Pest Scanner] Model {model_name} gagal: {model_err}")

    if not ai_analysis:
        db_scan.status = "failed"
        db_scan.result_label = f"Gagal dianalisis: {str(last_error)[:150]}"
        db.commit()
        raise HTTPException(
            status_code=502,
            detail="Analisis AI gagal — layanan Gemini tidak dapat dihubungi atau kuota habis. Coba beberapa saat lagi.",
        )

    # 4. Update DB dengan hasil analisis aktual
    # (bisa diperhalus dengan Regex di produksi)
    confidence_score = 0.90 if "sehat" not in ai_analysis.lower() else 0.99

    db_scan.status = "processed"
    db_scan.result_label = ai_analysis
    db_scan.confidence_score = confidence_score
    db.commit()
    db.refresh(db_scan)

    return db_scan
