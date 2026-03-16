import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

# Gunakan direktori persist dari .env atau default lokal
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY tidak ditemukan di file .env. Harap isi terlebih dahulu.")
    exit(1)

def ingest_documents():
    print("Menyiapkan Pangkalan Pengetahuan (ChromaDB) untuk RAG...")
    
    # 1. Inisialisasi ChromaDB Client
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    
    # 2. Setup Gemini Embedding Function
    # Text embedding 004 adalah model standar Google untuk task RAG
    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=GEMINI_API_KEY,
        task_type="RETRIEVAL_DOCUMENT"
    )
    
    # 3. Buat atau dapatkan Collection
    collection_name = "cocopra_knowledge_base"
    try:
        # Hapus jika sudah ada agar bersih tiap kali script dijalankan
        client.delete_collection(name=collection_name)
    except Exception:
        pass # Collection belum ada
        
    collection = client.create_collection(
        name=collection_name, 
        embedding_function=gemini_ef
    )
    
    # 4. Baca dokumen teks mentah (SOP kelapa)
    doc_path = os.path.join(os.path.dirname(__file__), "data", "permentan_kelapa_mock.txt")
    
    if not os.path.exists(doc_path):
        print(f"File dokumen tidak ditemukan di: {doc_path}")
        return
        
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    # 5. Chunking sederhana (Pisah berdasarkan paragraf ganda atau header)
    # Dalam produksi riil, gunakan LangChain RecursiveCharacterTextSplitter
    raw_chunks = text.split("\n\n")
    chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 50]
    
    # 6. Masukkan ke ChromaDB
    ids = [f"doc_{i}" for i in range(len(chunks))]
    metadatas = [{"source": "Permentan & SOP Dinas Pertanian"} for _ in range(len(chunks))]
    
    print(f"Mengekstrak {len(chunks)} chunk ke dimensi vektor...")
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    
    print("Ingestion Selesai! Pangkalan Pengetahuan Hukum Pertanian sudah aktif.")

if __name__ == "__main__":
    ingest_documents()
