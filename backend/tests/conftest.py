# ============================================================
# Konfigurasi pytest global — dijalankan SEBELUM modul test diimport
# ============================================================

import os

# Semua test memakai database SQLite terpisah (bukan cocopra.db milik dev)
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_cocopra.db")

# Pastikan test berjalan tanpa memanggil API eksternal
os.environ.pop("GEMINI_API_KEY", None)
