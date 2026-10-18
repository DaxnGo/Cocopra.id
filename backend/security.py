# ============================================================
# COCOPRA.ID — Utilitas Keamanan (Hashing Password & Token JWT)
# ============================================================

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

# Secret key WAJIB di-set lewat .env di production
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    JWT_SECRET_KEY = "cocopra-development-secret-please-change-in-production"
    print(
        "Warning: JWT_SECRET_KEY tidak di-set di .env — memakai secret default. "
        "JANGAN dipakai di production!"
    )
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # default 24 jam

_BCRYPT_PREFIXES = ("$2a$", "$2b$", "$2y$")


def _password_bytes(password: str) -> bytes:
    """Batasi ke 72 byte — batas maksimum bcrypt."""
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    """Hash password dengan bcrypt."""
    return bcrypt.hashpw(_password_bytes(password), bcrypt.gensalt()).decode("utf-8")


def is_password_hashed(stored: str) -> bool:
    """True jika nilai di kolom password sudah berupa hash bcrypt."""
    return bool(stored) and stored.startswith(_BCRYPT_PREFIXES)


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Verifikasi password.
    Mendukung password lama yang masih plaintext (data MVP awal)
    agar user lama tetap bisa login dan otomatis di-upgrade ke hash.
    """
    if is_password_hashed(stored_password):
        try:
            return bcrypt.checkpw(_password_bytes(plain_password), stored_password.encode("utf-8"))
        except ValueError:
            return False
    return plain_password == stored_password


def create_access_token(username: str, role: str) -> str:
    """Buat JWT dengan masa berlaku ACCESS_TOKEN_EXPIRE_MINUTES."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode & validasi JWT.
    Raise jwt.ExpiredSignatureError jika kedaluwarsa,
    atau jwt.PyJWTError jika tidak valid.
    """
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
