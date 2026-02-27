from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever, MultiQueryRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from src.config import Config
from src.prompts import RAG_PROMPT
import logging

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MotorRAG")

class MotorRAG:
    """
    Motor RAG de grado producción con arquitectura Modular.
    Implementa Hybrid Search (Vector + BM25), Multi-Query Expansion y Cross-Encoder Re-ranking.
    """
    def __init__(self):
        self._initialize_components()
        self._setup_retriever()
        self._build_chain()

    def _initialize_components(self):
        """Inicializa los modelos y la base de datos."""
        logger.info("Inicializando componentes del Motor RAG...")
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.vector_db = Chroma(
            persist_directory=Config.PERSIST_DIRECTORY,
            embedding_function=self.embeddings
        )
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            openai_api_key=Config.OPENAI_API_KEY
        )

    def _setup_retriever(self):
        """Configura el pipeline de recuperación multinivel."""
        logger.info("Configurando pipeline de recuperación híbrida...")
        
        # 1. Recuperador Vectorial (Densidad Semántica)
        vector_retriever = self.vector_db.as_retriever(search_kwargs={"k": 15})

        # 2. Recuperador BM25 (Léxico/Palabras Clave)
        all_docs_data = self.vector_db.get()
        if all_docs_data and len(all_docs_data['documents']) > 0:
            from langchain_core.documents import Document
            docs = [
                Document(page_content=doc, metadata=meta) 
                for doc, meta in zip(all_docs_data['documents'], all_docs_data['metadatas'])
            ]
            bm25_retriever = BM25Retriever.from_documents(docs)
            bm25_retriever.k = 10
            
            # Fusión Híbrida (Ensemble)
            ensemble_retriever = EnsembleRetriever(
                retrievers=[bm25_retriever, vector_retriever],
                weights=[0.3, 0.7] # Prioridad a lo semántico, apoyo en palabras clave
            )
        else:
            logger.warning("No hay documentos en la DB. Usando solo recuperador vectorial.")
            ensemble_retriever = vector_retriever

        # 3. Multi-Query Expansion (Para capturar matices en la pregunta)
        mq_retriever = MultiQueryRetriever.from_llm(
            retriever=ensemble_retriever,
            llm=self.llm
        )

        # 4. Re-ranking (Cross-Encoder para máxima precisión)
        try:
            compressor = FlashrankRerank(model=Config.RERANK_MODEL)
            self.retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=mq_retriever
            )
            logger.info("Re-ranker (Flashrank) activado con éxito.")
        except Exception as e:
            logger.error(f"Error al cargar Re-ranker: {e}. Usando fallback.")
            self.retriever = mq_retriever

    def _build_chain(self):
        """Construye la cadena de ejecución usando LCEL."""
        
        def format_docs(docs):
            return "\n\n".join(f"[Fuente: {d.metadata.get('source', 'N/A')}]\n{d.page_content}" for d in docs)

        self.chain = (
            RunnableParallel({
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough(),
                "docs": self.retriever # Mantenemos los docs para extraer fuentes después
            })
            | {
                "respuesta": RAG_PROMPT | self.llm | StrOutputParser(),
                "fuentes": lambda x: [d.metadata.get("source", "Desconocida") for d in x["docs"]]
            }
        )

    def responder(self, pregunta: str):
        """Ejecuta la cadena RAG para una pregunta dada."""
        logger.info(f"Procesando consulta: {pregunta}")
        try:
            # En LCEL, invoke devuelve directamente el diccionario estructurado definido en la cadena
            resultado = self.chain.invoke(pregunta)
            
            return {
                "respuesta": resultado["respuesta"],
                "fuentes": list(set(resultado["fuentes"]))
            }
        except Exception as e:
            logger.error(f"Error en el motor: {e}")
            return {
                "respuesta": "Lo siento, ocurrió un error técnico al procesar tu solicitud.",
                "fuentes": []
            }

if __name__ == "__main__":
    # Test rápido de integración
    motor = MotorRAG()
    res = motor.responder("¿Qué información principal contienen los documentos?")
    print(f"\n--- TEST OUTPUT ---\nRespuesta: {res['respuesta']}\nFuentes: {res['fuentes']}")
