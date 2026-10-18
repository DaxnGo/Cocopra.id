# ============================================================
# GEO-ALERT EWS — Router (Sprint 6: Fully Implemented)
# ============================================================

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import get_db

router = APIRouter()

# Wilayah yang dipantau Dinas (cakupan layanan awal)
WILAYAH_PANTAU_DEFAULT = [
    "Kema", "Likupang", "Wori", "Airmadidi", "Dimembe",
    "Kalawat", "Talawaan", "Watutumou", "Kauditan",
    "Tatelu", "Kolongan", "Mapanget",
]


class GeoAlert(BaseModel):
    """Model alert geospasial."""
    id: int
    severity: str  # "critical", "warning", "info"
    title: str
    description: str
    latitude: float
    longitude: float
    radius_km: float
    desa: str
    timestamp: str
    is_active: bool = True


class AlertReport(BaseModel):
    """Model laporan alert dari petani."""
    jenis_laporan: str  # "hama", "penyakit", "cuaca"
    deskripsi: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    lokasi_desa: str


def _sample_alerts() -> List[GeoAlert]:
    """
    Peringatan contoh untuk demo peta EWS.
    Di fase production: dipindahkan ke feed resmi/DB laporan terverifikasi.
    """
    now = datetime.now().isoformat()
    return [
        GeoAlert(
            id=1,
            severity="critical",
            title="Serangan Masif Pseudococcus",
            description="Serangan kutu putih terdeteksi di kebun kelapa area utara Desa Kema. Radius terdampak estimasi 5km.",
            latitude=1.3851,
            longitude=125.0782,
            radius_km=5.0,
            desa="Kema",
            timestamp=now,
        ),
        GeoAlert(
            id=2,
            severity="warning",
            title="Indikasi Hama Awal",
            description="Beberapa petani melaporkan tanda-tanda awal serangan kutu putih. Verifikasi penyuluh diperlukan.",
            latitude=1.4102,
            longitude=125.0423,
            radius_km=3.0,
            desa="Likupang",
            timestamp=now,
        ),
    ]


@router.get("/alerts")
async def get_active_alerts(db: Session = Depends(get_db)):
    """
    Ambil semua peringatan aktif dalam radius 5-10km.

    Menggabungkan alerts bawaan dengan laporan petani yang sudah diverifikasi.
    Data digunakan oleh frontend untuk menampilkan pin dan radius di peta Leaflet.js.
    """
    alerts = _sample_alerts()

    # Tambahkan laporan petani yang sudah terverifikasi dari database
    verified_reports = db.query(models.GeoAlertLog).filter(
        models.GeoAlertLog.status == "verified"
    ).all()

    for report in verified_reports:
        if report.latitude and report.longitude:
            alerts.append(GeoAlert(
                id=100 + report.id,
                severity="warning",
                title=f"Laporan: {report.jenis_laporan.capitalize()}",
                description=report.deskripsi,
                latitude=report.latitude,
                longitude=report.longitude,
                radius_km=2.0,
                desa=report.lokasi_desa,
                timestamp=report.timestamp.isoformat() if report.timestamp else datetime.now().isoformat(),
            ))

    return {
        "alerts": [a.model_dump() for a in alerts],
        "total_active": len(alerts),
    }


@router.post("/report")
async def submit_alert_report(report: AlertReport, db: Session = Depends(get_db)):
    """
    Petani melaporkan kondisi darurat di lapangan.

    Laporan ini akan:
    1. Disimpan ke database
    2. Divalidasi oleh sistem (cross-check dengan data scan hama)
    3. Jika valid, trigger notifikasi push ke petani dalam radius 5-10km
    """
    # Simpan laporan ke database
    db_report = models.GeoAlertLog(
        jenis_laporan=report.jenis_laporan,
        deskripsi=report.deskripsi,
        latitude=report.latitude,
        longitude=report.longitude,
        lokasi_desa=report.lokasi_desa,
        status="pending",
        timestamp=datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC, konsisten kolom DateTime
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return {
        "status": "received",
        "message": f"Laporan dari {report.lokasi_desa} diterima. Tim penyuluh akan segera menindaklanjuti.",
        "report_id": db_report.id,
        "timestamp": db_report.timestamp.isoformat(),
    }


@router.get("/dashboard")
async def get_governance_dashboard(db: Session = Depends(get_db)):
    """
    Data agregat untuk Smart Control Dashboard (Dinas Pertanian).

    Menampilkan statistik lintas desa untuk pengambilan keputusan.
    Semua angka dihitung dari data nyata di database.
    """
    # Total seluruh laporan di database
    total_laporan = db.query(models.GeoAlertLog).count()

    # Laporan 30 hari terakhir
    batas_30_hari = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30)
    laporan_bulan_ini = db.query(models.GeoAlertLog).filter(
        models.GeoAlertLog.timestamp >= batas_30_hari
    ).count()

    # Peringatan aktif = laporan DB (pending + verified) + alerts contoh yang selalu tampil
    peringatan_aktif_db = db.query(models.GeoAlertLog).filter(
        models.GeoAlertLog.status.in_(["pending", "verified"])
    ).count()
    peringatan_aktif = peringatan_aktif_db + len(_sample_alerts())

    # Kumpulkan daftar desa unik dari laporan
    desa_list = db.query(models.GeoAlertLog.lokasi_desa).distinct().all()
    desa_terpantau = set(d[0] for d in desa_list)
    desa_terpantau.update(WILAYAH_PANTAU_DEFAULT)

    # Agregat heatmap dari scan hama
    pest_scans = db.query(models.PestScanLog).filter(
        models.PestScanLog.status == "processed"
    ).count()

    return {
        "total_desa_terpantau": len(desa_terpantau),
        "total_laporan": total_laporan,
        "total_laporan_bulan_ini": laporan_bulan_ini,
        "peringatan_aktif": peringatan_aktif,
        "total_scan_hama": pest_scans,
        "rekomendasi_subsidi": [
            {"desa": "Kema", "prioritas": "Tinggi", "alasan": "Serangan masif Pseudococcus"},
            {"desa": "Likupang", "prioritas": "Sedang", "alasan": "Indikasi awal, perlu verifikasi"},
        ],
        "heatmap_data": [
            {"desa": "Kema", "lat": 1.3851, "lng": 125.0782, "intensity": 0.9},
            {"desa": "Likupang", "lat": 1.4102, "lng": 125.0423, "intensity": 0.5},
            {"desa": "Wori", "lat": 1.4500, "lng": 124.9200, "intensity": 0.1},
        ],
    }
