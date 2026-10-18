from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# --- Pest Scanner Schemas ---
class PestScanCreate(BaseModel):
    image_data: str
    filename: str
    timestamp: datetime

class PestScanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: str
    result_label: Optional[str] = None
    confidence_score: Optional[float] = None

# --- Info Harga Schemas ---
class HargaCreate(BaseModel):
    harga: int
    lokasi: str
    pembeli: Optional[str] = None
    timestamp: datetime

class HargaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    harga: int
    lokasi: str
    pembeli: Optional[str] = None
    is_anomaly: bool
    timestamp: datetime

# --- Auth Schemas ---
class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

# Frontend-compatible auth response format
class UserInfo(BaseModel):
    name: str
    role: str
    email: Optional[str] = None
    phone: Optional[str] = None
    village: Optional[str] = None

class AuthResponse(BaseModel):
    token: str
    user: UserInfo

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=6, max_length=72)  # 72 = batas maksimum bcrypt
    village: Optional[str] = None
    role: str = "petani"  # Diabaikan server: registrasi publik selalu role "petani"

class UserResponse(BaseModel):
    user: UserInfo

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    village: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str = Field(min_length=6, max_length=72)  # 72 = batas maksimum bcrypt

# --- Regulatory Schemas ---
class PesticideResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nama_pestisida: str
    kategori: Optional[str] = None
    nama_perusahaan: Optional[str] = None
    bahan_aktif: Optional[str] = None
