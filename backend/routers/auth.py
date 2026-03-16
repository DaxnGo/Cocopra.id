from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import Optional

router = APIRouter()


def _get_user_from_token(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """
    Ekstrak user dari token sederhana.
    Format token MVP: cocopra_token_{role}_{username}_999
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token tidak ditemukan")
    
    token = authorization.replace("Bearer ", "")
    parts = token.split("_")
    # cocopra_token_{role}_{username}_999
    if len(parts) < 4 or parts[0] != "cocopra" or parts[1] != "token":
        raise HTTPException(status_code=401, detail="Token tidak valid")
    
    username = parts[3]
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user


def _make_token(user):
    """Generate token sederhana untuk MVP."""
    return f"cocopra_token_{user.role}_{user.username}_999"


def _user_info(user):
    """Convert User model ke UserInfo dict sesuai format frontend."""
    return {
        "name": user.nama_lengkap or user.username,
        "role": user.role,
        "email": user.email or "",
        "phone": user.phone or "",
        "village": user.village or "",
    }


@router.post("/login")
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Autentikasi User (Petani / Dinas Pertanian).
    Mendukung login via username ATAU email.
    Response format sesuai frontend: { token, user: { name, role, email, ... } }
    """
    # Cari user — support both username and email
    username = login_data.username or login_data.email
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username atau email harus diisi"
        )

    user = db.query(models.User).filter(models.User.username == username).first()
    
    # Jika tidak ketemu via username, coba cari via email
    if not user and login_data.email:
        user = db.query(models.User).filter(models.User.email == login_data.email).first()

    if not user or user.password_hash != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "token": _make_token(user),
        "user": _user_info(user),
    }


@router.post("/register")
def register(reg_data: schemas.RegisterRequest, db: Session = Depends(get_db)):
    """
    Registrasi user baru.
    Response format sesuai frontend: { token, user }
    """
    # The frontend uses email for login, so we use email as the unique username
    existing = db.query(models.User).filter(
        (models.User.username == reg_data.email) | (models.User.email == reg_data.email)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar"
        )

    new_user = models.User(
        username=reg_data.email, # Use email as the main identifier
        email=reg_data.email,    # Store email separately as well
        password_hash=reg_data.password,  # MVP: plaintext, production: hash
        role=reg_data.role,
        nama_lengkap=reg_data.name,
        village=reg_data.village,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "token": _make_token(new_user),
        "user": _user_info(new_user),
    }


@router.get("/me")
def get_me(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Ambil data user saat ini berdasarkan token.
    Response: { user: { name, role, email, phone, village } }
    """
    user = _get_user_from_token(authorization, db)
    return {"user": _user_info(user)}


@router.put("/update-profile")
def update_profile(
    profile_data: schemas.UpdateProfileRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Update profil user (nama, email, phone, village).
    """
    user = _get_user_from_token(authorization, db)

    if profile_data.name is not None:
        user.nama_lengkap = profile_data.name
    if profile_data.email is not None:
        user.email = profile_data.email
    if profile_data.phone is not None:
        user.phone = profile_data.phone
    if profile_data.village is not None:
        user.village = profile_data.village

    db.commit()
    db.refresh(user)

    return {
        "message": "Profil berhasil diperbarui",
        "user": _user_info(user),
    }


@router.put("/change-password")
def change_password(
    pwd_data: schemas.ChangePasswordRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Ganti password user setelah verifikasi password lama.
    """
    user = _get_user_from_token(authorization, db)

    # Verifikasi password lama
    if user.password_hash != pwd_data.currentPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password saat ini salah"
        )

    user.password_hash = pwd_data.newPassword  # MVP: plaintext
    db.commit()

    return {"message": "Password berhasil diperbarui"}
