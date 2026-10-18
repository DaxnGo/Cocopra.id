# ============================================================
# COCOPRA.ID - Security & AI Integration Tests
# ============================================================
# Mencakup: auth (bcrypt + JWT), harga, pest scanner (fake AI),
# assistant RAG (fake AI), dan embedding function Gemini.
# Tidak ada panggilan API eksternal di sini.
# ============================================================

import base64
import io
from datetime import datetime, timedelta, timezone

import jwt as pyjwt
import pytest
from fastapi.testclient import TestClient
from PIL import Image as PILImage

import models
from database import Base, SessionLocal, engine
from main import app
from security import JWT_ALGORITHM, JWT_SECRET_KEY


@pytest.fixture(autouse=True)
def _fresh_db():
    """Tabel bersih untuk setiap test (database test terpisah, lihat conftest.py)."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def _login(client, email, password):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


# ============================================================
# 1. AUTH — bcrypt + JWT
# ============================================================

class TestAuth:
    def test_seed_login_and_jwt_shape(self):
        with TestClient(app) as client:
            r = _login(client, "petani1", "password123")
            assert r.status_code == 200
            token = r.json()["token"]
            assert token.count(".") == 2  # format JWT

            r = client.get("/api/auth/me", headers=_auth_header(token))
            assert r.status_code == 200
            assert r.json()["user"]["role"] == "petani"

    def test_seed_password_stored_hashed(self):
        with TestClient(app) as client:
            _login(client, "dinas_minut", "admin123")  # pastikan seed berjalan
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.username == "dinas_minut").first()
        assert user.password_hash.startswith("$2")  # bcrypt
        db.close()

    def test_login_wrong_password(self):
        with TestClient(app) as client:
            assert _login(client, "petani1", "salah").status_code == 401

    def test_forged_legacy_token_rejected(self):
        with TestClient(app) as client:
            r = client.get("/api/auth/me", headers=_auth_header("cocopra_token_petani_petani1_999"))
            assert r.status_code == 401

    def test_garbage_token_rejected(self):
        with TestClient(app) as client:
            r = client.get("/api/auth/me", headers=_auth_header("abc.def.ghi"))
            assert r.status_code == 401

    def test_expired_token_rejected(self):
        expired = pyjwt.encode(
            {
                "sub": "petani1",
                "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
            },
            JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )
        with TestClient(app) as client:
            r = client.get("/api/auth/me", headers=_auth_header(expired))
            assert r.status_code == 401
            assert "berakhir" in r.json()["detail"].lower()

    def test_register_short_password_rejected(self):
        with TestClient(app) as client:
            r = client.post("/api/auth/register", json={
                "name": "X", "email": "x@x.com", "password": "123"
            })
            assert r.status_code == 422

    def test_register_forces_petani_role(self):
        with TestClient(app) as client:
            r = client.post("/api/auth/register", json={
                "name": "Petani Baru", "email": "baru@cocopra.id",
                "password": "rahasia123", "role": "dinas", "village": "Kema",
            })
            assert r.status_code == 200
            assert r.json()["user"]["role"] == "petani"

    def test_register_duplicate_email(self):
        with TestClient(app) as client:
            payload = {"name": "Dup", "email": "dup@cocopra.id", "password": "rahasia123"}
            assert client.post("/api/auth/register", json=payload).status_code == 200
            assert client.post("/api/auth/register", json=payload).status_code == 400

    def test_change_password_flow(self):
        with TestClient(app) as client:
            token = client.post("/api/auth/register", json={
                "name": "Ganti Pass", "email": "ganti@cocopra.id", "password": "rahasia123"
            }).json()["token"]

            # Password lama salah -> 400
            r = client.put("/api/auth/change-password",
                           json={"currentPassword": "salah", "newPassword": "gantipass1"},
                           headers=_auth_header(token))
            assert r.status_code == 400

            # Password lama benar -> 200
            r = client.put("/api/auth/change-password",
                           json={"currentPassword": "rahasia123", "newPassword": "gantipass1"},
                           headers=_auth_header(token))
            assert r.status_code == 200

            # Login pakai password baru OK, password lama ditolak
            assert _login(client, "ganti@cocopra.id", "gantipass1").status_code == 200
            assert _login(client, "ganti@cocopra.id", "rahasia123").status_code == 401

    def test_legacy_plaintext_password_auto_upgraded(self):
        with TestClient(app) as client:
            db = SessionLocal()
            db.add(models.User(username="legacy@cocopra.id", email="legacy@cocopra.id",
                               password_hash="plainlama", role="petani", nama_lengkap="Legacy"))
            db.commit()
            db.close()

            assert _login(client, "legacy@cocopra.id", "plainlama").status_code == 200

        db = SessionLocal()
        user = db.query(models.User).filter(models.User.username == "legacy@cocopra.id").first()
        assert user.password_hash.startswith("$2")  # otomatis di-hash
        db.close()

    def test_update_profile_duplicate_email_rejected(self):
        with TestClient(app) as client:
            token = client.post("/api/auth/register", json={
                "name": "Profil", "email": "profil@cocopra.id", "password": "rahasia123"
            }).json()["token"]

            # Bentrok dengan username user seed
            r = client.put("/api/auth/update-profile", json={"email": "petani1"},
                           headers=_auth_header(token))
            assert r.status_code == 400

            # Update normal
            r = client.put("/api/auth/update-profile", json={"name": "Nama Baru", "village": "Wori"},
                           headers=_auth_header(token))
            assert r.status_code == 200
            assert r.json()["user"]["name"] == "Nama Baru"


# ============================================================
# 2. PEST SCANNER — tanpa hasil palsu, fallback antar-model
# ============================================================

def _tiny_png_data_url() -> str:
    buf = io.BytesIO()
    PILImage.new("RGB", (8, 8), (0, 128, 0)).save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


class TestPestScanner:
    def test_scan_without_api_key_returns_503(self):
        with TestClient(app) as client:
            r = client.post("/api/pest/scan", json={
                "image_data": "data:image/png;base64,AAAA",
                "filename": "daun.png",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            assert r.status_code == 503
            assert "GEMINI_API_KEY" in r.json()["detail"]

    def test_scan_success_with_model_fallback(self, monkeypatch):
        import routers.pest as pest_module

        calls = []

        class FakeModels:
            def generate_content(self, *, model, contents):
                calls.append(model)
                if model == pest_module.MODEL_CANDIDATES[0]:
                    raise RuntimeError("model pertama sedang sibuk")
                class R:
                    text = "Tanaman terserang Kutu Putih (Pseudococcus) dengan keyakinan 95%."
                return R()

        class FakeClient:
            models = FakeModels()

        monkeypatch.setattr(pest_module, "_gemini_client", FakeClient())

        with TestClient(app) as client:
            r = client.post("/api/pest/scan", json={
                "image_data": _tiny_png_data_url(),
                "filename": "daun.png",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "processed"
        assert "Kutu Putih" in body["result_label"]
        # model pertama gagal -> fallback ke model kedua
        assert calls == [pest_module.MODEL_CANDIDATES[0], pest_module.MODEL_CANDIDATES[1]]

    def test_scan_invalid_image_returns_400(self, monkeypatch):
        import routers.pest as pest_module

        class FakeClient:
            models = None  # tidak dipakai untuk payload invalid

        monkeypatch.setattr(pest_module, "_gemini_client", FakeClient())

        with TestClient(app) as client:
            r = client.post("/api/pest/scan", json={
                "image_data": "bukan-data-url",
                "filename": "x.png",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        assert r.status_code == 400

    def test_scan_all_models_fail_returns_502(self, monkeypatch):
        import routers.pest as pest_module

        class FakeModels:
            def generate_content(self, *, model, contents):
                raise RuntimeError("semua model down")

        class FakeClient:
            models = FakeModels()

        monkeypatch.setattr(pest_module, "_gemini_client", FakeClient())

        with TestClient(app) as client:
            r = client.post("/api/pest/scan", json={
                "image_data": _tiny_png_data_url(),
                "filename": "daun.png",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        assert r.status_code == 502

        # Hasil gagal tercatat di DB demi audit
        db = SessionLocal()
        row = db.query(models.PestScanLog).order_by(models.PestScanLog.id.desc()).first()
        assert row.status == "failed"
        db.close()


# ============================================================
# 3. ASSISTANT RAG — dengan AI palsu (tanpa panggilan API)
# ============================================================

class TestAssistant:
    def test_chat_without_config_returns_local_message(self):
        with TestClient(app) as client:
            r = client.post("/api/assistant/chat", json={"history": [], "message": "halo"})
            assert r.status_code == 200
        # Tanpa GEMINI_API_KEY: tidak boleh ada jawaban AI palsu
        assert "SISTEM LOKAL" in r.json()["reply"]

    def test_chat_with_fake_ai_detects_regulation_flag(self, monkeypatch):
        import routers.assistant as assistant

        captured = {}

        class FakeChat:
            def send_message(self, msg):
                class R:
                    text = "[PERINGATAN REGULASI] Monokrotofos dilarang oleh Permentan."
                return R()

        class FakeChats:
            def create(self, *, model, config, history):
                captured["model"] = model
                captured["system_instruction"] = config.system_instruction
                captured["history"] = history
                return FakeChat()

        class FakeClient:
            chats = FakeChats()

        class FakeCollection:
            def query(self, query_texts, n_results):
                return {"documents": [["Monokrotofos dilarang oleh Permentan No. 39/2015."]]}

        monkeypatch.setattr(assistant, "genai_client", FakeClient())
        monkeypatch.setattr(assistant, "collection", FakeCollection())

        with TestClient(app) as client:
            r = client.post("/api/assistant/chat", json={
                "history": [{"role": "user", "parts": "halo"}],
                "message": "boleh pakai monokrotofos?",
            })

        assert r.status_code == 200
        body = r.json()
        assert body["regulatory_flag"] is True
        # Konteks RAG ikut disuntikkan ke system prompt
        assert "Monokrotofos dilarang" in captured["system_instruction"]


# ============================================================
# 4. EMBEDDING FUNCTION GEMINI — kontrak ChromaDB (tanpa API)
# ============================================================

class TestGeminiEmbeddingFunction:
    def test_embedding_contract_offline(self, monkeypatch):
        import gemini_embeddings as ge

        class FakeEmbedding:
            def __init__(self, values):
                self.values = values

        class FakeResponse:
            embeddings = [FakeEmbedding([0.1, 0.2]), FakeEmbedding([0.3, 0.4])]

        captured = {}

        class FakeModels:
            def embed_content(self, *, model, contents, config):
                captured.update(model=model, contents=contents, task_type=config.task_type)
                return FakeResponse()

        class FakeClient:
            models = FakeModels()

        ef = ge.GeminiEmbeddingFunction(api_key="dummy", task_type="RETRIEVAL_QUERY")
        ef._client = FakeClient()

        result = ef(["teks satu", "teks dua"])
        # ChromaDB membungkus hasil sebagai numpy array — bandingkan sebagai list
        assert [list(values) for values in result] == [[0.1, 0.2], [0.3, 0.4]]
        assert captured["model"] == "text-embedding-004"
        assert captured["task_type"] == "RETRIEVAL_QUERY"

        # Kontrak ChromaDB
        assert ef.name() == "cocopra-gemini-embedding"
        assert ef.get_config() == {"model": "text-embedding-004"}
        # build_from_config membaca GEMINI_API_KEY dari environment
        monkeypatch.setenv("GEMINI_API_KEY", "dummy")
        rebuilt = ge.GeminiEmbeddingFunction.build_from_config({"model": "text-embedding-004"})
        assert rebuilt.model == "text-embedding-004"
