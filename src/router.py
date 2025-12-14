"""
Sistema de routing inteligente para clasificar consultas.
Determina qué tipo de herramienta usar para responder cada consulta.
"""

import logging
import re
from enum import Enum
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.config import LLM_MODEL, LLM_TEMPERATURE

logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Tipos de consultas que el sistema puede manejar."""

    BALANCE = "balance"  # Consulta de balance en CSV
    KNOWLEDGE = "knowledge"  # Consulta a base de conocimientos
    GENERAL = "general"  # Pregunta general para el LLM


class QueryRouter:
    """Router inteligente para clasificar y enrutar consultas."""

    def __init__(self, llm_model: str = LLM_MODEL, temperature: float = 0.0):
        """
        Inicializa el router de consultas.

        Args:
            llm_model: Modelo de LLM a usar
            temperature: Temperatura para el LLM (0 para determinista)
        """
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        self._setup_routing_prompt()
        logger.info("QueryRouter inicializado")

    def _setup_routing_prompt(self) -> None:
        """Configura el prompt para clasificación de consultas."""
        self.routing_prompt = PromptTemplate(
            input_variables=["query"],
            template="""Eres un asistente bancario que clasifica consultas de clientes.

Clasifica la siguiente consulta en UNA de estas categorías:

1. "balance" - Si el cliente pregunta por el saldo, balance o estado de cuenta específico
   Ejemplos: 
   - "¿Cuál es mi balance?"
   - "¿Cuánto dinero tengo en mi cuenta?"
   - "Balance de la cédula V-12345678"
   - "Consultar saldo"

2. "knowledge" - Si el cliente pregunta sobre procedimientos, servicios o información bancaria general
   Ejemplos:
   - "¿Cómo abrir una cuenta?"
   - "¿Cómo solicitar una tarjeta de crédito?"
   - "¿Cómo hacer una transferencia?"
   - "¿Qué requisitos necesito para...?"
   - "Información sobre cuentas de ahorro"

3. "general" - Si la pregunta no está relacionada con el banco o es una consulta general
   Ejemplos:
   - "¿Qué hora es?"
   - "¿Cuál es el sentido de la vida?"
   - "Hola"
   - "Gracias"

Consulta del cliente: "{query}"

Responde ÚNICAMENTE con una palabra: "balance", "knowledge" o "general"
Tu respuesta:""",
        )

    def classify_query(self, query: str) -> QueryType:
        """
        Clasifica una consulta en uno de los tipos definidos.

        Args:
            query: Consulta del usuario

        Returns:
            Tipo de consulta (QueryType)
        """
        # Primero intentar clasificación basada en reglas (más rápido)
        rule_based = self._rule_based_classification(query)
        if rule_based:
            logger.info(f"Clasificación basada en reglas: {rule_based.value}")
            return rule_based

        # Si no hay match en reglas, usar LLM
        logger.info("Usando LLM para clasificación")
        try:
            formatted_prompt = self.routing_prompt.format(query=query)
            response = self.llm.invoke(formatted_prompt)
            classification = response.content.strip().lower()

            # Mapear respuesta a QueryType
            if "balance" in classification:
                query_type = QueryType.BALANCE
            elif "knowledge" in classification:
                query_type = QueryType.KNOWLEDGE
            else:
                query_type = QueryType.GENERAL

            logger.info(f"Consulta clasificada como: {query_type.value}")
            return query_type

        except Exception as e:
            logger.error(f"Error en clasificación: {e}")
            # Default a GENERAL en caso de error
            return QueryType.GENERAL

    def _rule_based_classification(self, query: str) -> QueryType | None:
        """
        Clasificación basada en reglas simples (más rápida).

        Args:
            query: Consulta del usuario

        Returns:
            QueryType si se puede clasificar, None si no
        """
        query_lower = query.lower()

        # Patrones para BALANCE
        balance_keywords = [
            r"balance",
            r"saldo",
            r"cuanto.*dinero",
            r"cuanto.*tengo",
            r"estado.*cuenta",
            r"consultar.*cuenta",
            r"cedula.*v-\d+",
            r"cédula.*v-\d+",
        ]

        for pattern in balance_keywords:
            if re.search(pattern, query_lower):
                return QueryType.BALANCE

        # Patrones para KNOWLEDGE
        knowledge_keywords = [
            r"como.*abrir.*cuenta",
            r"como.*solicitar.*tarjeta",
            r"como.*transferir",
            r"como.*hacer.*transferencia",
            r"requisitos.*para",
            r"informacion.*sobre",
            r"información.*sobre",
            r"que.*necesito.*para",
            r"pasos.*para",
            r"procedimiento",
            r"tarjeta.*credito",
            r"tarjeta.*crédito",
            r"cuenta.*ahorro",
        ]

        for pattern in knowledge_keywords:
            if re.search(pattern, query_lower):
                return QueryType.KNOWLEDGE

        # Si contiene cédula venezolana, es balance
        if re.search(r"v-\d{7,8}", query_lower):
            return QueryType.BALANCE

        return None

    def extract_cedula(self, query: str) -> str | None:
        """
        Extrae número de cédula de una consulta.

        Args:
            query: Consulta del usuario

        Returns:
            Número de cédula en formato "V-XXXXXXXX" o None
        """
        # Buscar patrón de cédula venezolana
        patterns = [
            r"(V-\d{7,8})",
            r"v-(\d{7,8})",
            r"cedula\s*(\d{7,8})",
            r"cédula\s*(\d{7,8})",
        ]

        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                cedula = match.group(1) if match.lastindex == 1 else match.group(0)
                # Normalizar formato
                cedula = cedula.upper()
                if not cedula.startswith("V-"):
                    cedula = f"V-{cedula.replace('V-', '').replace('v-', '')}"
                logger.info(f"Cédula extraída: {cedula}")
                return cedula

        logger.warning("No se pudo extraer cédula de la consulta")
        return None

    def get_routing_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas de routing (para debugging).

        Returns:
            Diccionario con contadores de cada tipo
        """
        # En una implementación real, esto mantendría contadores
        return {"balance": 0, "knowledge": 0, "general": 0}
