from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False) # In real app, this MUST be hashed
    role = Column(String, nullable=False) # "petani" or "dinas"
    nama_lengkap = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    village = Column(String, nullable=True)

class PestScanLog(Base):
    __tablename__ = "pest_scan_logs"

    id = Column(Integer, primary_key=True, index=True)
    image_data = Column(String, nullable=False) # In real prod, this stores object storage URL
    filename = Column(String, nullable=False)
    result_label = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    status = Column(String, default="pending") # pending, processed, failed
    timestamp = Column(DateTime, default=datetime.utcnow)

class HargaLog(Base):
    __tablename__ = "harga_logs"

    id = Column(Integer, primary_key=True, index=True)
    harga = Column(Integer, nullable=False)
    lokasi = Column(String, nullable=False)
    pembeli = Column(String, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GeoAlertLog(Base):
    __tablename__ = "geo_alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    jenis_laporan = Column(String, nullable=False)  # "hama", "penyakit", "cuaca"
    deskripsi = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    lokasi_desa = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, verified, resolved
    timestamp = Column(DateTime, default=datetime.utcnow)

class PesticideRegistry(Base):
    __tablename__ = "pesticide_registry"
    
    id = Column(Integer, primary_key=True, index=True)
    nama_pestisida = Column(String, index=True, nullable=False)
    kategori = Column(String, index=True, nullable=True)
    nama_perusahaan = Column(String, nullable=True)
    bahan_aktif = Column(String, nullable=True)
