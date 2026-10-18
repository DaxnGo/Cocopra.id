# ============================================================
# COCOPRA.ID - Comprehensive API Test Suite (Sprint 6)
# ============================================================
# Run: python -m pytest test_endpoints.py -v
# ============================================================

# Setup: Use test database (in-memory SQLite)
import os
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_cocopra.db"

from database import Base, engine
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Buat tabel baru sebelum setiap test, hapus setelahnya."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ============================================================
# 1. SYSTEM ENDPOINTS
# ============================================================

class TestSystem:
    def test_root(self):
        """Root endpoint harus mengembalikan info API."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Cocopra" in data["message"]

    def test_health_check(self):
        """Health check harus OK."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "cocopra-api"
        assert "version" in data


# ============================================================
# 2. HARGA ENDPOINTS
# ============================================================

class TestHarga:
    def _submit_harga(self, harga=8500, lokasi="Desa Airmadidi", pembeli="Tengkulak A"):
        payload = {
            "harga": harga,
            "lokasi": lokasi,
            "pembeli": pembeli,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return client.post("/api/harga/", json=payload)

    def test_submit_harga_normal(self):
        """Harga normal (7000-12000) tidak seharusnya anomaly."""
        response = self._submit_harga(harga=8500)
        assert response.status_code == 200
        data = response.json()
        assert data["harga"] == 8500
        assert data["lokasi"] == "Desa Airmadidi"
        assert not data["is_anomaly"]

    def test_submit_harga_anomaly_high(self):
        """Harga terlalu tinggi (>15000) harus di-flag sebagai anomaly."""
        response = self._submit_harga(harga=20000)
        assert response.status_code == 200
        data = response.json()
        assert data["is_anomaly"]

    def test_submit_harga_anomaly_low(self):
        """Harga terlalu rendah (<5000) harus di-flag sebagai anomaly."""
        response = self._submit_harga(harga=2000)
        assert response.status_code == 200
        data = response.json()
        assert data["is_anomaly"]

    def test_get_harga_list(self):
        """GET /api/harga/ harus mengembalikan list."""
        self._submit_harga(harga=8500)
        self._submit_harga(harga=9000)
        response = client.get("/api/harga/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_get_harga_trend_with_data(self):
        """Trend harus mengembalikan data dari DB jika ada."""
        self._submit_harga(harga=8500)
        self._submit_harga(harga=9000)
        response = client.get("/api/harga/trend")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert "date" in data[0]
        assert "harga" in data[0]

    def test_get_harga_trend_empty(self):
        """Trend harus mengembalikan list kosong jika DB kosong (tanpa data palsu)."""
        response = client.get("/api/harga/trend")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_harga_median_with_data(self):
        """Median harus dihitung dari data di DB."""
        self._submit_harga(harga=8000)
        self._submit_harga(harga=9000)
        self._submit_harga(harga=10000)
        response = client.get("/api/harga/median")
        assert response.status_code == 200
        data = response.json()
        assert data["median"] == 9000
        assert data["count"] == 3
        assert data["min"] == 8000
        assert data["max"] == 10000
        assert data["source"] == "database"

    def test_get_harga_median_even(self):
        """Median dengan jumlah data genap harus dihitung dari 2 nilai tengah."""
        self._submit_harga(harga=8000)
        self._submit_harga(harga=9000)
        self._submit_harga(harga=10000)
        self._submit_harga(harga=11000)
        response = client.get("/api/harga/median")
        assert response.status_code == 200
        data = response.json()
        assert data["median"] == 9500
        assert data["count"] == 4
        assert data["source"] == "database"

    def test_get_harga_median_empty(self):
        """Tanpa data, median harus kosong yang jelas (bukan angka palsu)."""
        response = client.get("/api/harga/median")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "empty"
        assert data["count"] == 0
        assert data["median"] is None


# ============================================================
# 3. GEO-ALERT ENDPOINTS
# ============================================================

class TestGeo:
    def test_get_alerts(self):
        """Harus mengembalikan setidaknya alerts default."""
        response = client.get("/api/geo/alerts")
        assert response.status_code == 200
        data = response.json()
        assert "alerts" in data
        assert "total_active" in data
        assert len(data["alerts"]) >= 2  # Minimal 2 default alerts

    def test_submit_report(self):
        """Laporan petani harus tersimpan dan mendapat response."""
        payload = {
            "jenis_laporan": "hama",
            "deskripsi": "Kutu putih ditemukan di kebun blok B",
            "latitude": 1.39,
            "longitude": 125.07,
            "lokasi_desa": "Kema"
        }
        response = client.post("/api/geo/report", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "received"
        assert data["report_id"] > 0
        assert "Kema" in data["message"]

    def test_get_dashboard(self):
        """Dashboard governance harus mengembalikan statistik."""
        response = client.get("/api/geo/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "total_desa_terpantau" in data
        assert "total_laporan_bulan_ini" in data
        assert "peringatan_aktif" in data
        assert data["total_desa_terpantau"] > 0

    def test_report_affects_dashboard(self):
        """Setelah submit laporan, dashboard stats harus berubah."""
        # Get baseline
        dash_before = client.get("/api/geo/dashboard").json()

        # Submit a report
        payload = {
            "jenis_laporan": "penyakit",
            "deskripsi": "Daun kelapa menguning masif",
            "lokasi_desa": "Talawaan"
        }
        client.post("/api/geo/report", json=payload)

        # Check dashboard updated
        dash_after = client.get("/api/geo/dashboard").json()
        assert dash_after["total_laporan_bulan_ini"] > dash_before["total_laporan_bulan_ini"]


# ============================================================
# 4. PEST SCANNER ENDPOINTS (Tanpa Gemini API call)
# ============================================================

class TestPestScanner:
    def test_scan_without_api_key(self):
        """
        Tanpa GEMINI_API_KEY, scan harus ditolak dengan 503 yang jelas
        (bukan mengembalikan hasil analisis palsu).
        """
        payload = {
            "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ==",
            "filename": "test_leaf.jpg",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        response = client.post("/api/pest/scan", json=payload)
        assert response.status_code == 503
        assert "GEMINI_API_KEY" in response.json()["detail"]

    def test_scan_invalid_image_format(self):
        """Key tersedia tapi payload bukan data URL valid -> 400 (bukan hasil palsu)."""
        import routers.pest as pest_module

        class _FakeModels:
            def generate_content(self, **kwargs):  # tidak boleh terpanggil
                raise AssertionError("AI tidak boleh dipanggil untuk payload invalid")

        class _FakeClient:
            models = _FakeModels()

        original = pest_module._gemini_client
        pest_module._gemini_client = _FakeClient()
        try:
            payload = {
                "image_data": "bukan-data-url",
                "filename": "x.jpg",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            response = client.post("/api/pest/scan", json=payload)
            assert response.status_code == 400
        finally:
            pest_module._gemini_client = original
