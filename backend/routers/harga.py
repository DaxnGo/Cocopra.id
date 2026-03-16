from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List
from datetime import datetime

router = APIRouter()

# Mock Isolation Forest Anomaly Detection
def mock_anomaly_detection(harga: int) -> bool:
    # Asumsikan harga normal kopra ada di rentang 7000 - 12000
    if harga < 5000 or harga > 15000:
        return True # Anomaly
    return False

@router.post("/", response_model=schemas.HargaResponse)
def submit_harga(harga_data: schemas.HargaCreate, db: Session = Depends(get_db)):
    """
    Menerima input crowdsourced harga harian kopra dari petani/tengkulak,
    menyimpannya di database, dan nge-flag jika ada anomali harga.
    """
    # 1. Cek anomali (Intelligence for Justice)
    is_anomaly = mock_anomaly_detection(harga_data.harga)

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
def get_harga(db: Session = Depends(get_db), limit: int = 50):
    """
    Mengambil data riwayat harga dari database.
    """
    records = db.query(models.HargaLog).order_by(models.HargaLog.timestamp.desc()).limit(limit).all()
    return records

@router.get("/trend")
def get_harga_trend(db: Session = Depends(get_db)):
    """
    End-point untuk grafik Visualisasi Harga (Recharts).
    Jika data kosong, kembalikan mock data.
    """
    records = db.query(models.HargaLog).order_by(models.HargaLog.timestamp.asc()).all()
    
    if not records:
        return [
            {"date": "1 Mar", "harga": 8100},
            {"date": "5 Mar", "harga": 8250},
            {"date": "10 Mar", "harga": 8000},
            {"date": "15 Mar", "harga": 8400},
            {"date": "20 Mar", "harga": 8500},
            {"date": "25 Mar", "harga": 8650},
            {"date": "30 Mar", "harga": 8600}
        ]
        
    trend_data = []
    for r in records:
        try:
            dt = datetime.fromisoformat(r.timestamp.replace('Z', '+00:00')) if isinstance(r.timestamp, str) else r.timestamp
            date_str = dt.strftime("%d %b")
        except Exception:
            date_str = "Unknown"
            
        trend_data.append({
            "date": date_str,
            "harga": r.harga
        })
    return trend_data

@router.get("/median")
def get_harga_median(db: Session = Depends(get_db)):
    """
    Menghitung median harga regional berdasarkan seluruh data di database.
    Digunakan oleh frontend untuk menampilkan indeks bargaining power.
    """
    records = db.query(models.HargaLog.harga).all()
    
    if not records:
        return {
            "median": 8350,
            "count": 7,
            "min": 8000,
            "max": 8650,
            "source": "mock"
        }
    
    harga_list = sorted([r[0] for r in records])
    n = len(harga_list)
    
    if n % 2 == 0:
        median = (harga_list[n // 2 - 1] + harga_list[n // 2]) / 2
    else:
        median = harga_list[n // 2]
    
    return {
        "median": int(median),
        "count": n,
        "min": min(harga_list),
        "max": max(harga_list),
        "source": "database"
    }
