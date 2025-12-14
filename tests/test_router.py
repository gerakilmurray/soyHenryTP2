"""
Tests unitarios para el sistema de routing.
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.router import QueryRouter, QueryType


@pytest.fixture
def router():
    """Fixture para crear una instancia del QueryRouter."""
    return QueryRouter()


class TestQueryRouter:
    """Tests para QueryRouter."""

    def test_initialization(self, router):
        """Test que el router se inicializa correctamente."""
        assert router is not None
        assert router.llm is not None

    # Tests de clasificación de BALANCE
    def test_classify_balance_with_cedula(self, router):
        """Test clasificación de consulta de balance con cédula."""
        queries = [
            "¿Cuál es el balance de la cédula V-12345678?",
            "Consultar saldo V-87654321",
            "Balance de cuenta V-11111111",
        ]

        for query in queries:
            result = router.classify_query(query)
            assert result == QueryType.BALANCE

    def test_classify_balance_keywords(self, router):
        """Test clasificación con palabras clave de balance."""
        queries = [
            "¿Cuánto dinero tengo en mi cuenta?",
            "Consultar mi saldo",
            "Estado de cuenta",
        ]

        for query in queries:
            result = router.classify_query(query)
            assert result == QueryType.BALANCE

    # Tests de clasificación de KNOWLEDGE
    def test_classify_knowledge_opening_account(self, router):
        """Test clasificación de consultas sobre abrir cuenta."""
        queries = [
            "¿Cómo abrir una cuenta de ahorros?",
            "Como puedo abrir una cuenta?",
            "Pasos para abrir cuenta",
        ]

        for query in queries:
            result = router.classify_query(query)
            assert result == QueryType.KNOWLEDGE

    def test_classify_knowledge_credit_card(self, router):
        """Test clasificación de consultas sobre tarjetas de crédito."""
        queries = [
            "¿Cómo solicitar una tarjeta de crédito?",
            "Información sobre tarjetas de credito",
            "Requisitos para tarjeta de crédito",
        ]

        for query in queries:
            result = router.classify_query(query)
            assert result == QueryType.KNOWLEDGE

    def test_classify_knowledge_transfer(self, router):
        """Test clasificación de consultas sobre transferencias."""
        queries = [
            "¿Cómo hacer una transferencia?",
            "Como transferir dinero",
            "Procedimiento para transferir",
        ]

        for query in queries:
            result = router.classify_query(query)
            assert result == QueryType.KNOWLEDGE

    # Tests de clasificación GENERAL
    def test_classify_general(self, router):
        """Test clasificación de consultas generales."""
        queries = [
            "Hola",
            "¿Qué hora es?",
            "Gracias",
            "Adiós",
        ]

        for query in queries:
            result = router.classify_query(query)
            assert result == QueryType.GENERAL

    # Tests de extracción de cédula
    def test_extract_cedula_format_v_dash(self, router):
        """Test extracción de cédula en formato V-XXXXXXXX."""
        queries = [
            "Balance de V-12345678",
            "Consultar cédula V-87654321",
            "La cédula V-99999999",
        ]

        expected = ["V-12345678", "V-87654321", "V-99999999"]

        for query, expected_cedula in zip(queries, expected):
            result = router.extract_cedula(query)
            assert result == expected_cedula

    def test_extract_cedula_lowercase(self, router):
        """Test extracción de cédula en minúsculas."""
        query = "balance de v-12345678"
        result = router.extract_cedula(query)
        assert result == "V-12345678"

    def test_extract_cedula_without_v(self, router):
        """Test extracción de cédula sin V-."""
        query = "cedula 12345678"
        result = router.extract_cedula(query)
        assert result == "V-12345678"

    def test_extract_cedula_not_found(self, router):
        """Test cuando no se encuentra cédula."""
        query = "¿Cómo abrir una cuenta?"
        result = router.extract_cedula(query)
        assert result is None


class TestRuleBasedClassification:
    """Tests para clasificación basada en reglas."""

    def test_rule_based_balance(self, router):
        """Test clasificación rápida por reglas para balance."""
        query = "Balance de la cuenta V-12345678"
        result = router._rule_based_classification(query)
        assert result == QueryType.BALANCE

    def test_rule_based_knowledge(self, router):
        """Test clasificación rápida por reglas para knowledge."""
        query = "¿Cómo abrir una cuenta de ahorros?"
        result = router._rule_based_classification(query)
        assert result == QueryType.KNOWLEDGE

    def test_rule_based_no_match(self, router):
        """Test cuando no hay match en reglas."""
        query = "Hola, buenos días"
        result = router._rule_based_classification(query)
        assert result is None


# Tests de integración
class TestRouterIntegration:
    """Tests de integración para el router."""

    def test_multiple_classifications(self, router):
        """Test clasificaciones múltiples consecutivas."""
        test_cases = [
            ("Balance V-12345678", QueryType.BALANCE),
            ("¿Cómo abrir cuenta?", QueryType.KNOWLEDGE),
            ("Hola", QueryType.GENERAL),
        ]

        for query, expected_type in test_cases:
            result = router.classify_query(query)
            assert result == expected_type

    def test_edge_cases(self, router):
        """Test casos edge."""
        # Query vacía
        result = router.classify_query("")
        assert result in [QueryType.BALANCE, QueryType.KNOWLEDGE, QueryType.GENERAL]

        # Query muy larga
        long_query = "Hola " * 100 + "¿Cómo abrir una cuenta?"
        result = router.classify_query(long_query)
        assert result == QueryType.KNOWLEDGE
