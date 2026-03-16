# ============================================================
# COCOPRA.ID — FastAPI Backend Entry Point
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI App
app = FastAPI(
    title="Cocopra.id API",
    description="Backend API untuk platform agritech kelapa Cocopra.id — Minahasa Utara",
    version="1.0.0-mvp",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Middleware — Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local dev to avoid port conflicts
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Models Initialization ---
from database import engine, Base
import models

# Buat tabel SQLite jika belum ada
Base.metadata.create_all(bind=engine)

from routers import pest, harga, assistant, geo, auth, regulatory
from sqlalchemy.orm import Session
from database import SessionLocal

app.include_router(auth.router, prefix="/api/auth", tags=["Autentikasi User"])
app.include_router(pest.router, prefix="/api/pest", tags=["Pest-Vision Scanner"])
app.include_router(harga.router, prefix="/api/harga", tags=["Adil-Harga Ledger"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["RAG Agri-Assistant"])
app.include_router(geo.router, prefix="/api/geo", tags=["Geo-Alert EWS"])
app.include_router(regulatory.router, prefix="/api/regulatory", tags=["Regulatory Check"])

# --- Database Seed (Initialize Default Users) ---
@app.on_event("startup")
def startup_event():
    db: Session = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            user1 = models.User(username="petani1", password_hash="password123", role="petani", nama_lengkap="Kelompok Tani Harapan")
            user2 = models.User(username="dinas_minut", password_hash="admin123", role="dinas", nama_lengkap="Dinas Pertanian Minut")
            db.add(user1)
            db.add(user2)
            db.commit()
            print("Successfully seeded initial users to database (petani1 & dinas_minut)")
    except Exception as e:
        print(f"Failed to seed users: {e}")
    finally:
        db.close()

# --- Health Check ---
@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint untuk monitoring status server."""
    return {
        "status": "ok",
        "service": "cocopra-api",
        "version": "1.0.0-mvp",
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
