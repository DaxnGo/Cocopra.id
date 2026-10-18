import os
import traceback
from typing import List

import chromadb
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel

from gemini_embeddings import GeminiEmbeddingFunction

load_dotenv()

router = APIRouter()

# --- 1. RAG Configuration Setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
COLLECTION_NAME = "cocopra_knowledge_base"
CHAT_MODEL = "gemini-flash-latest"

genai_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

collection = None
if genai_client:
    _chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    try:
        collection = _chroma_client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=GeminiEmbeddingFunction(
                api_key=GEMINI_API_KEY,
                task_type="RETRIEVAL_QUERY",
            ),
        )
    except Exception:
        print("Warning: Collection belum dibuat. Jalankan `python rag_engine.py` terlebih dahulu.")


# --- 2. Request / Response Schemas ---
class ChatMessage(BaseModel):
    role: str  # "user" or "model"
    parts: str  # message content

class ChatRequest(BaseModel):
    history: List[ChatMessage]
    message: str

class ChatResponse(BaseModel):
    reply: str
    regulatory_flag: bool  # True if the AI detected illegal actions based on RAG context


@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(req: ChatRequest):
    """
    RAG Chatbot Endpoint.
    1. Retrieve relevant context from ChromaDB based on user message
    2. Inject context into Gemini System Prompt
    3. Generate accurate, hallucination-free answer
    """
    if genai_client is None or collection is None:
        return {
            "reply": "[SISTEM LOKAL]: API Key atau ChromaDB belum aktif. Mohon setel GEMINI_API_KEY dan jalankan rag_engine.py.",
            "regulatory_flag": False
        }

    # Step 1: Retrieval (Cari dokumen hukum terdekat dari ChromaDB)
    results = collection.query(
        query_texts=[req.message],
        n_results=3  # Ambil top 3 paragraf paling relevan
    )

    # Kumpulkan teks konteks
    context_text = ""
    documents = results.get("documents") or []
    if documents and documents[0]:
        for i, doc in enumerate(documents[0]):
            context_text += f"Pasal/SOP Kutipan {i+1}: {doc}\n"

    # Step 2: RAG Prompt Engineering (Anti-Halusinasi)
    system_prompt = f"""Anda adalah 'Asisten AI Cocopra.id', penyuluh pertanian cerdas untuk petani kelapa di Minahasa Utara.
    Jawaban Anda HARUS didasarkan pada dokumen hukum dan SOP berikut ini jika relevan:

    {context_text}

    Aturan tegas:
    1. Jika pengguna bertanya tentang dosis atau obat berbahaya, rujuk HANYA pada kutipan di atas.
    2. Apabila Anda mendapati instruksi pengguna melanggar aturan (misalnya memakai Monokrotofos), peringatkan dengan keras bahwa itu melanggar Permentan/Ilegal.
    3. Jika informasi yang ditanyakan sama sekali TIDAK ADA dalam kutipan di atas, beritahu bahwa Anda tidak memiliki informasi aturannya dalam SOP lokal, jangan mengarang.
    4. Jawab dalam Bahasa Indonesia yang ramah, ringkas, dan jelas.
    5. awali peringatan dengan [PERINGATAN REGULASI] jika ada pelanggaran hukum.
    """

    # Konversi format riwayat chat frontend ke format Gemini (google-genai)
    gemini_history = []
    for msg in req.history:
        role = msg.role if msg.role in ("user", "model") else "user"
        gemini_history.append(types.Content(role=role, parts=[types.Part(text=msg.parts)]))

    try:
        # Step 3: Generation (Gemini Flash)
        chat_session = genai_client.chats.create(
            model=CHAT_MODEL,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
            history=gemini_history,
        )
        response = chat_session.send_message(req.message)
        reply_text = response.text or ""

        # Cek apakah RAG menge-flag pelarangan regulasi
        regulatory_flag = "[PERINGATAN REGULASI]" in reply_text.upper()

        return ChatResponse(
            reply=reply_text,
            regulatory_flag=regulatory_flag
        )
    except Exception as e:
        traceback.print_exc()
        # Kembalikan error yang jelas — tanpa jawaban mock yang menyesatkan
        raise HTTPException(
            status_code=502,
            detail=f"Asisten AI sedang tidak dapat dihubungi (layanan Gemini bermasalah atau kuota habis): {str(e)[:120]}",
        ) from e
