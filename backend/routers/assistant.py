from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import os
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# --- 1. RAG Configuration Setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Init ChromaDB Client
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    
    # Init Embedding Function
    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=GEMINI_API_KEY,
        task_type="RETRIEVAL_QUERY"
    )
    
    # Connect to Collection
    try:
        collection = client.get_collection(
            name="cocopra_knowledge_base",
            embedding_function=gemini_ef
        )
    except Exception as e:
        print("Warning: Collection belum dibuat. Jalankan rag_engine.py terlebih dahulu.")
        collection = None

# --- 2. Request / Response Schemas ---
class ChatMessage(BaseModel):
    role: str # "user" or "model" 
    parts: str # message content

class ChatRequest(BaseModel):
    history: List[ChatMessage]
    message: str

class ChatResponse(BaseModel):
    reply: str
    regulatory_flag: bool # True if the AI detected illegal actions based on RAG context

@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(req: ChatRequest):
    """
    RAG Chatbot Endpoint.
    1. Retrieve relevant context from ChromaDB based on user message
    2. Inject context into Gemini System Prompt
    3. Generate accurate, hallucination-free answer
    """
    if not GEMINI_API_KEY or not collection:
        return {
            "reply": "[SISTEM LOKAL]: API Key atau ChromaDB belum aktif. Mohon setel GEMINI_API_KEY dan jalankan rag_engine.py.", 
            "regulatory_flag": False
        }

    # Step 1: Retrieval (Cari dokumen hukum terdekat dari ChromaDB)
    results = collection.query(
        query_texts=[req.message],
        n_results=3 # Ambil top 3 paragraf paling relevan
    )
    
    # Kumpulkan teks konteks
    context_text = ""
    if results['documents'] and len(results['documents']) > 0:
        for i, doc in enumerate(results['documents'][0]):
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

    try:
        # Step 3: Generation (Gemini Flash)
        model = genai.GenerativeModel(
            model_name='gemini-flash-latest',
            system_instruction=system_prompt
        )
        
        # Konversi Format Riwayat Chat frontend ke format Gemini
        gemini_history = []
        for msg in req.history:
            gemini_history.append({"role": msg.role, "parts": [msg.parts]})

        chat_session = model.start_chat(history=gemini_history)
        
        # Eksekusi RAG
        response = chat_session.send_message(req.message)
        reply_text = response.text
        
        # Cek apakah RAG menge-flag pelarangan regulasi
        regulatory_flag = "[PERINGATAN REGULASI]" in reply_text.upper()

        return ChatResponse(
            reply=reply_text,
            regulatory_flag=regulatory_flag
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Jika quota API Gemini habis (429) atau error lain, kembalikan mock response edukatif
        reply_msg = (
            "[MOCK MODE - API Quota Exceeded]\n\n"
            "Halo! Saat ini sistem AI sedang mencapai batas penggunaan. Sebagai referensi, "
            "jika Anda menghadapi Kendala Hama, hindari pestisida kimia keras tahap awal. "
            "Selalu gunakan musuh alami atau sabun cuci piring ringan sesuai SOP Pertanian Kelapa.\n\n"
            f"(Sistem Trace: {str(e)[:50]}...)"
        )
        return ChatResponse(
            reply=reply_msg,
            regulatory_flag=False
        )
