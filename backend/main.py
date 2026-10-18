# ============================================================
# COCOPRA.ID — FastAPI Backend Entry Point
# ============================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables DULU, sebelum import modul yang membaca env saat import
load_dotenv()

from database import engine, Base, SessionLocal  # noqa: E402
import models  # noqa: E402
from routers import pest, harga, assistant, geo, auth, regulatory  # noqa: E402
from security import hash_password  # noqa: E402

APP_VERSION = "1.0.0-mvp"

# Buat tabel SQLite jika belum ada
Base.metadata.create_all(bind=engine)


def _get_cors_origins():
    """Origin yang diizinkan: dari env FRONTEND_URL (boleh dipisah koma) + default dev lokal."""
    origins = [o.strip() for o in os.getenv("FRONTEND_URL", "").split(",") if o.strip()]
    dev_defaults = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]
    for origin in dev_defaults:
        if origin not in origins:
            origins.append(origin)
    return origins


def _seed_default_users():
    """Seed user awal (hanya jika tabel user masih kosong)."""
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            db.add_all([
                models.User(
                    username="petani1",
                    password_hash=hash_password("password123"),
                    role="petani",
                    nama_lengkap="Kelompok Tani Harapan",
                ),
                models.User(
                    username="dinas_minut",
                    password_hash=hash_password("admin123"),
                    role="dinas",
                    nama_lengkap="Dinas Pertanian Minut",
                ),
            ])
            db.commit()
            print("Seeded default users to database (petani1 & dinas_minut)")
    except Exception as e:
        db.rollback()
        print(f"Failed to seed users: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _seed_default_users()
    yield


# Initialize FastAPI App
app = FastAPI(
    title="Cocopra.id API",
    description="Backend API untuk platform agritech kelapa Cocopra.id — Minahasa Utara",
    version=APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS Middleware — hanya origin frontend yang dikenal
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Autentikasi User"])
app.include_router(pest.router, prefix="/api/pest", tags=["Pest-Vision Scanner"])
app.include_router(harga.router, prefix="/api/harga", tags=["Adil-Harga Ledger"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["RAG Agri-Assistant"])
app.include_router(geo.router, prefix="/api/geo", tags=["Geo-Alert EWS"])
app.include_router(regulatory.router, prefix="/api/regulatory", tags=["Regulatory Check"])


# --- Health Check ---
@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint untuk monitoring status server."""
    return {
        "status": "ok",
        "service": "cocopra-api",
        "version": APP_VERSION,
        "message": "Cocopra.id API berjalan normal 🌴",
    }


# --- Root ---
@app.get("/", tags=["System"])
async def root():
    """Root endpoint — redirect info."""
    return {
        "message": "Selamat datang di Cocopra.id API",
        "docs": "/api/docs",
        "health": "/api/health",
    }
