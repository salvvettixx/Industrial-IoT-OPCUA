import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from src.config import Config

class Ingestor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )

    def load_documents(self):
        documents = []
        for file in os.listdir(Config.DATA_PATH):
            full_path = os.path.join(Config.DATA_PATH, file)
            if file.endswith(".pdf"):
                loader = PyPDFLoader(full_path)
                documents.extend(loader.load())
            elif file.endswith(".docx"):
                loader = Docx2txtLoader(full_path)
                documents.extend(loader.load())
            elif file.endswith(".txt"):
                loader = TextLoader(full_path)
                documents.extend(loader.load())
        return documents

    def create_vector_store(self):
        print(f"Ingestando documentos desde {Config.DATA_PATH}...")
        raw_docs = self.load_documents()
        if not raw_docs:
            print("No se encontraron documentos para procesar.")
            return None
        
        chunks = self.text_splitter.split_documents(raw_docs)
        print(f"Creados {len(chunks)} fragmentos.")
        
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=Config.PERSIST_DIRECTORY
        )
        vector_db.persist()
        print(f"Base de datos vectorial guardada en {Config.PERSIST_DIRECTORY}")
        return vector_db

if __name__ == "__main__":
    ingestor = Ingestor()
    ingestor.create_vector_store()
