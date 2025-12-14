"""
Módulo de Base de Conocimientos (Knowledge Base).
Implementa RAG (Retrieval-Augmented Generation) usando FAISS y embeddings.
"""
import logging
from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_core.documents import Document
from src.config import EMBEDDINGS_MODEL_NAME, KNOWLEDGE_BASE_DIR, INDEX_DIR, RETRIEVER_K

logger = logging.getLogger(__name__)


class KnowledgeBaseManager:
    """Gestor de la base de conocimientos vectorial."""
    
    def __init__(
        self,
        index_path: Path = INDEX_DIR,
        knowledge_base_path: Path = KNOWLEDGE_BASE_DIR,
        embeddings_model: str = EMBEDDINGS_MODEL_NAME,
        k: int = RETRIEVER_K
    ):
        """
        Inicializa el gestor de base de conocimientos.
        
        Args:
            index_path: Ruta al índice FAISS
            knowledge_base_path: Ruta a los documentos de conocimiento
            embeddings_model: Nombre del modelo de embeddings
            k: Número de documentos a recuperar
        """
        self.index_path = index_path
        self.knowledge_base_path = knowledge_base_path
        self.embeddings_model_name = embeddings_model
        self.k = k
        
        # Inicializar embeddings
        logger.info(f"Cargando modelo de embeddings: {embeddings_model}")
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)
        
        # Cargar o crear índice
        self.vectorstore: Optional[FAISS] = None
        self._load_or_create_index()
    
    def _load_or_create_index(self) -> None:
        """Carga el índice FAISS existente o crea uno nuevo."""
        try:
            if self.index_path.exists():
                logger.info(f"Cargando índice existente desde: {self.index_path}")
                self.vectorstore = FAISS.load_local(
                    str(self.index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Índice cargado exitosamente")
            else:
                logger.warning(f"Índice no encontrado en {self.index_path}")
                logger.info("Creando nuevo índice desde documentos...")
                self.create_index()
        except Exception as e:
            logger.error(f"Error al cargar índice: {e}")
            raise
    
    def create_index(self) -> None:
        """Crea un nuevo índice FAISS desde los documentos de conocimiento."""
        try:
            # Cargar documentos
            logger.info(f"Cargando documentos desde: {self.knowledge_base_path}")
            loader = DirectoryLoader(
                str(self.knowledge_base_path),
                glob="**/*.txt"
            )
            docs = loader.load()
            logger.info(f"Documentos cargados: {len(docs)}")
            
            if not docs:
                raise ValueError(f"No se encontraron documentos en {self.knowledge_base_path}")
            
            # Crear vectorstore
            logger.info("Creando vectorstore FAISS...")
            self.vectorstore = FAISS.from_documents(docs, self.embeddings)
            
            # Guardar índice
            self.index_path.mkdir(parents=True, exist_ok=True)
            self.vectorstore.save_local(str(self.index_path))
            logger.info(f"Índice guardado en: {self.index_path}")
            
        except Exception as e:
            logger.error(f"Error al crear índice: {e}")
            raise
    
    def search(self, query: str, k: Optional[int] = None) -> List[Document]:
        """
        Busca documentos relevantes en la base de conocimientos.
        
        Args:
            query: Consulta de búsqueda
            k: Número de documentos a recuperar (usa self.k si no se especifica)
            
        Returns:
            Lista de documentos relevantes
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        k = k or self.k
        logger.info(f"Buscando en base de conocimientos: '{query}' (k={k})")
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"Encontrados {len(results)} documentos relevantes")
            return results
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            raise
    
    def search_with_score(self, query: str, k: Optional[int] = None) -> List[tuple]:
        """
        Busca documentos con scores de relevancia.
        
        Args:
            query: Consulta de búsqueda
            k: Número de documentos a recuperar
            
        Returns:
            Lista de tuplas (documento, score)
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        k = k or self.k
        logger.info(f"Buscando con scores: '{query}' (k={k})")
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            for doc, score in results:
                logger.debug(f"Documento encontrado con score {score:.4f}")
            return results
        except Exception as e:
            logger.error(f"Error en búsqueda con scores: {e}")
            raise
    
    def get_retriever(self):
        """
        Obtiene un retriever de LangChain para usar en chains.
        
        Returns:
            Retriever configurado
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        return self.vectorstore.as_retriever(search_kwargs={"k": self.k})
    
    def reload_index(self) -> None:
        """Recarga el índice desde disco."""
        logger.info("Recargando índice...")
        self._load_or_create_index()
    
    def get_all_documents(self) -> List[Document]:
        """
        Obtiene todos los documentos en el vectorstore.
        
        Returns:
            Lista de todos los documentos
        """
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        # FAISS no tiene método directo para esto, pero podemos hacer una búsqueda amplia
        # Esta es una aproximación
        return self.search("información bancaria", k=100)


def format_knowledge_response(documents: List[Document], query: str) -> str:
    """
    Formatea documentos recuperados para presentación.
    
    Args:
        documents: Lista de documentos recuperados
        query: Consulta original
        
    Returns:
        String formateado
    """
    if not documents:
        return "No se encontró información relevante en la base de conocimientos."
    
    response = f"📚 **Información encontrada sobre: {query}**\n\n"
    
    for i, doc in enumerate(documents, 1):
        content = doc.page_content.strip()
        source = doc.metadata.get("source", "Desconocido")
        
        response += f"**Fuente {i}:** {Path(source).name}\n"
        response += f"{content}\n\n"
        response += "─" * 50 + "\n\n"
    
    return response
