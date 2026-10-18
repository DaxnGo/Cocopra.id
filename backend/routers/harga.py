from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter()

# Rentang harga kopra yang wajar (Rp/kg) — di luar ini dianggap anomali.
# MVP: aturan ambang sederhana. Produksi: model Isolation Forest pada data historis.
HARGA_MIN_WAJAR = 5000
HARGA_MAX_WAJAR = 15000

# Batas jumlah titik data untuk grafik trend
MAX_TREND_POINTS = 200


def is_price_anomaly(harga: int) -> bool:
    return harga < HARGA_MIN_WAJAR or harga > HARGA_MAX_WAJAR


@router.post("/", response_model=schemas.HargaResponse)
def submit_harga(harga_data: schemas.HargaCreate, db: Session = Depends(get_db)):
    """
    Menerima input crowdsourced harga harian kopra dari petani/tengkulak,
    menyimpannya di database, dan nge-flag jika ada anomali harga.
    """
    # 1. Cek anomali (Intelligence for Justice)
    is_anomaly = is_price_anomaly(harga_data.harga)

    # 2. Simpan ke database
    db_harga = models.HargaLog(
        harga=harga_data.harga,
        lokasi=harga_data.lokasi,
        pembeli=harga_data.pembeli,
        timestamp=harga_data.timestamp,
        is_anomaly=is_anomaly
    )
    db.add(db_harga)
    db.commit()
    db.refresh(db_harga)

    return db_harga


@router.get("/", response_model=List[schemas.HargaResponse])
def get_harga(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=500)):
    """
    Mengambil data riwayat harga dari database (default 50 terbaru, maksimal 500).
    """
    records = db.query(models.HargaLog).order_by(models.HargaLog.timestamp.desc()).limit(limit).all()
    return records


@router.get("/trend")
def get_harga_trend(db: Session = Depends(get_db)):
    """
    Data grafik harga: maksimal 200 titik terbaru.
    Jika belum ada data, kembalikan list kosong — frontend menampilkan
    grafik contoh dengan penanda "data contoh" (tanpa data palsu di API).
    """
    records = (
        db.query(models.HargaLog)
        .order_by(models.HargaLog.timestamp.desc())
        .limit(MAX_TREND_POINTS)
        .all()
    )
    records.reverse()  # urutkan dari paling lama ke terbaru

    trend_data = []
    for r in records:
        ts = r.timestamp
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                ts = None
        date_str = ts.strftime("%d %b") if ts else "Unknown"

        trend_data.append({
            "date": date_str,
            "harga": r.harga
        })
    return trend_data


@router.get("/median")
def get_harga_median(db: Session = Depends(get_db)):
    """
    Menghitung median harga regional berdasarkan seluruh data di database.
    Dihitung lewat query SQL (hanya mengambil baris median), tanpa memuat
    seluruh tabel ke memori.
    """
    count, harga_min, harga_max = db.query(
        func.count(models.HargaLog.id),
        func.min(models.HargaLog.harga),
        func.max(models.HargaLog.harga),
    ).one()

    if not count:
        return {
            "median": None,
            "count": 0,
            "min": None,
            "max": None,
            "source": "empty"
        }

    # Ambil 1 baris tengah (ganjil) atau 2 baris tengah (genap) via SQL
    offset = (count - 1) // 2
    limit = 2 if count % 2 == 0 else 1
    rows = (
        db.query(models.HargaLog.harga)
        .order_by(models.HargaLog.harga)
        .offset(offset)
        .limit(limit)
        .all()
    )
    values = [row[0] for row in rows]
    median = sum(values) / len(values)

    return {
        "median": int(median),
        "count": count,
        "min": harga_min,
        "max": harga_max,
        "source": "database"
    }
