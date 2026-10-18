# ============================================================
# COCOPRA.ID — Embedding Function Gemini untuk ChromaDB
# Dibangun di atas SDK google-genai (SDK lama google-generativeai
# sudah legacy/deprecated).
# ============================================================

import os

from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions import register_embedding_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DEFAULT_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")


@register_embedding_function
class GeminiEmbeddingFunction(EmbeddingFunction[Documents]):
    """
    Embedding Gemini (google-genai) untuk ChromaDB.

    Selalu di-pass eksplisit ke create_collection/get_collection.
    `get_config` sengaja tidak memuat task_type (beda antara ingestion dan query)
    agar konfigurasi collection tetap konsisten.
    """

    def __init__(self, api_key=None, task_type: str = "RETRIEVAL_QUERY", model=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY belum di-set — embedding Gemini tidak dapat dipakai.")
        self.task_type = task_type
        self.model = model or DEFAULT_EMBED_MODEL
        self._client = genai.Client(api_key=self.api_key)

    def __call__(self, input: Documents) -> Embeddings:
        """Embed daftar teks; dipanggil ChromaDB saat add/query."""
        texts = [str(t) for t in input]
        if not texts:
            return []
        result = self._client.models.embed_content(
            model=self.model,
            contents=texts,
            config=types.EmbedContentConfig(task_type=self.task_type),
        )
        return [embedding.values for embedding in result.embeddings]

    @staticmethod
    def name() -> str:
        """Nama unik fungsi embedding untuk ChromaDB (wajib staticmethod)."""
        return "cocopra-gemini-embedding"

    def default_space(self) -> str:
        """Embedding Gemini dinormalisasi — cosine adalah metrik yang disarankan."""
        return "cosine"

    def get_config(self):
        return {"model": self.model}

    @staticmethod
    def build_from_config(config):
        return GeminiEmbeddingFunction(model=config.get("model"))
