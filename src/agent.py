"""
Sistema principal de atención al cliente.
Integra todos los componentes: router, CSV, knowledge base y LLM.
"""

import logging
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from src.config import LLM_MODEL, LLM_TEMPERATURE
from src.router import QueryRouter, QueryType
from src.csv_query import CSVQueryManager, format_balance_response
from src.knowledge_base import KnowledgeBaseManager, format_knowledge_response

logger = logging.getLogger(__name__)


class CustomerServiceAgent:
    """Agente principal de atención al cliente."""

    def __init__(
        self, llm_model: str = LLM_MODEL, temperature: float = LLM_TEMPERATURE
    ):
        """
        Inicializa el agente de atención al cliente.

        Args:
            llm_model: Modelo de LLM a usar
            temperature: Temperatura para respuestas generales
        """
        logger.info("Inicializando CustomerServiceAgent...")

        # Componentes principales
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        self.router = QueryRouter(llm_model=llm_model)
        self.csv_manager = CSVQueryManager()
        self.kb_manager = KnowledgeBaseManager()

        # Chain para knowledge base
        self._setup_knowledge_chain()

        # Estadísticas
        self.stats = {
            "balance_queries": 0,
            "knowledge_queries": 0,
            "general_queries": 0,
            "total_queries": 0,
        }

        logger.info("CustomerServiceAgent inicializado exitosamente")

    def _setup_knowledge_chain(self) -> None:
        """Configura el chain para consultas a la base de conocimientos."""
        prompt_template = """Eres un asistente bancario experto y amigable de BANCO HENRY.
Usa la siguiente información para responder la pregunta del cliente de manera clara y profesional.

Contexto de la base de conocimientos:
{context}

Pregunta del cliente: {question}

Proporciona una respuesta detallada y útil basándote en el contexto. Si la información no está en el contexto, indícalo amablemente.

Respuesta:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        self.knowledge_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.kb_manager.get_retriever(),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True,
            verbose=True,
        )

    def process_query(self, query: str) -> Dict[str, any]:
        """
        Procesa una consulta del cliente y genera una respuesta.

        Args:
            query: Consulta del cliente

        Returns:
            Diccionario con la respuesta y metadatos
        """
        logger.info(f"Procesando consulta: '{query}'")
        self.stats["total_queries"] += 1

        try:
            # Clasificar la consulta
            query_type = self.router.classify_query(query)

            # Procesar según el tipo
            if query_type == QueryType.BALANCE:
                return self._handle_balance_query(query)
            elif query_type == QueryType.KNOWLEDGE:
                return self._handle_knowledge_query(query)
            else:  # GENERAL
                return self._handle_general_query(query)

        except Exception as e:
            logger.error(f"Error procesando consulta: {e}", exc_info=True)
            return {
                "success": False,
                "query_type": "error",
                "response": f"Lo siento, ocurrió un error al procesar tu consulta: {str(e)}",
                "error": str(e),
            }

    def _handle_balance_query(self, query: str) -> Dict[str, any]:
        """Maneja consultas de balance."""
        logger.info("Procesando consulta de BALANCE")
        self.stats["balance_queries"] += 1

        # Extraer cédula
        cedula = self.router.extract_cedula(query)

        if not cedula:
            # Intentar obtener cédula del LLM
            cedula = self._ask_llm_for_cedula(query)

        if not cedula:
            return {
                "success": False,
                "query_type": "balance",
                "response": "Por favor, proporciona un número de cédula válido para consultar el balance. Ejemplo: V-12345678",
                "needs_clarification": True,
            }

        try:
            balance_info = self.csv_manager.get_balance_by_cedula(cedula)

            return {
                "success": balance_info["found"],
                "query_type": "balance",
                "response": format_balance_response(balance_info),
                "data": balance_info,
                "cedula": cedula,
            }
        except Exception as e:
            logger.error(f"Error consultando balance: {e}")
            return {
                "success": False,
                "query_type": "balance",
                "response": f"Error al consultar el balance: {str(e)}",
                "error": str(e),
            }

    def _handle_knowledge_query(self, query: str) -> Dict[str, any]:
        """Maneja consultas a la base de conocimientos."""
        logger.info("Procesando consulta de KNOWLEDGE BASE")
        self.stats["knowledge_queries"] += 1

        try:
            # Usar el chain de RetrievalQA
            result = self.knowledge_chain.invoke({"query": query})

            return {
                "success": True,
                "query_type": "knowledge",
                "response": result["result"],
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "source": doc.metadata.get("source", "Unknown"),
                    }
                    for doc in result.get("source_documents", [])
                ],
            }
        except Exception as e:
            logger.error(f"Error en knowledge query: {e}")
            return {
                "success": False,
                "query_type": "knowledge",
                "response": f"Error al buscar en la base de conocimientos: {str(e)}",
                "error": str(e),
            }

    def _handle_general_query(self, query: str) -> Dict[str, any]:
        """Maneja consultas generales usando el LLM."""
        logger.info("Procesando consulta GENERAL")
        self.stats["general_queries"] += 1

        try:
            # Crear prompt contextualizado
            prompt = f"""Eres un asistente bancario amigable y profesional de BANCO HENRY.

El cliente te ha hecho la siguiente pregunta general: "{query}"

Responde de manera cortés y útil. Si la pregunta no está relacionada con el banco, responde brevemente y amablemente, recordándole que estás disponible para ayudarle con consultas bancarias.

Tu respuesta:"""

            response = self.llm.invoke(prompt)

            return {
                "success": True,
                "query_type": "general",
                "response": response.content,
            }
        except Exception as e:
            logger.error(f"Error en general query: {e}")
            return {
                "success": False,
                "query_type": "general",
                "response": f"Error al procesar la consulta: {str(e)}",
                "error": str(e),
            }

    def _ask_llm_for_cedula(self, query: str) -> Optional[str]:
        """Intenta extraer cédula usando el LLM."""
        try:
            prompt = f"""Extrae el número de cédula venezolana de la siguiente consulta.
Si encuentras un número de cédula, responde ÚNICAMENTE con el número en formato "V-XXXXXXXX".
Si no encuentras ninguna cédula, responde "NONE".

Consulta: "{query}"

Cédula:"""

            response = self.llm.invoke(prompt)
            cedula = response.content.strip()

            if cedula != "NONE" and cedula.startswith("V-"):
                return cedula
        except Exception as e:
            logger.error(f"Error extrayendo cédula con LLM: {e}")

        return None

    def get_statistics(self) -> Dict[str, any]:
        """
        Obtiene estadísticas de uso del sistema.

        Returns:
            Diccionario con estadísticas
        """
        return {
            **self.stats,
            "success_rate": (
                (self.stats["total_queries"] - self.stats.get("errors", 0))
                / self.stats["total_queries"]
                * 100
                if self.stats["total_queries"] > 0
                else 0
            ),
        }

    def reset_statistics(self) -> None:
        """Reinicia las estadísticas."""
        self.stats = {
            "balance_queries": 0,
            "knowledge_queries": 0,
            "general_queries": 0,
            "total_queries": 0,
        }
        logger.info("Estadísticas reiniciadas")
