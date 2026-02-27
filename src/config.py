import os
from dotenv import load_dotenv

# Fix for OpenBLAS memory error on Windows
os.environ["OPENBLAS_NUM_THREADS"] = "1"

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "./chroma_db")
    DATA_PATH = os.getenv("DATA_PATH", "./data")
    
    # Parámetros de Embedding y Re-ranking
    # Usamos OpenAI para Embeddings (debes tener la API Key en .env)
    RERANK_MODEL = "ms-marco-TinyBERT-L-2-v2" # Modelo ligero de Cross-Encoder
