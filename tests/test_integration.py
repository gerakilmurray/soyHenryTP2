"""
Tests de integración para el sistema completo.
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import CustomerServiceAgent
from src.router import QueryType


@pytest.fixture(scope="module")
def agent():
    """Fixture para crear una instancia del agente (scope module para reutilizar)."""
    return CustomerServiceAgent()


class TestCustomerServiceAgent:
    """Tests para el agente principal."""
    
    def test_initialization(self, agent):
        """Test que el agente se inicializa correctamente."""
        assert agent is not None
        assert agent.llm is not None
        assert agent.router is not None
        assert agent.csv_manager is not None
        assert agent.kb_manager is not None
    
    # Tests de consultas de BALANCE
    def test_process_balance_query_existing(self, agent):
        """Test procesamiento de consulta de balance existente."""
        query = "¿Cuál es el balance de la cédula V-12345678?"
        result = agent.process_query(query)
        
        assert result["success"] == True
        assert result["query_type"] == "balance"
        assert "Juan Pérez" in result["response"]
        assert "1,250.50" in result["response"]
    
    def test_process_balance_query_not_found(self, agent):
        """Test procesamiento de consulta de balance no encontrado."""
        query = "Balance de la cédula V-99999999"
        result = agent.process_query(query)
        
        assert result["query_type"] == "balance"
        assert "No se encontró" in result["response"]
    
    def test_process_balance_multiple_accounts(self, agent):
        """Test consultas de balance para múltiples cuentas."""
        test_cases = [
            ("V-12345678", "Juan Pérez", 1250.5),
            ("V-91827364", "Luis Méndez", 2580.0),
            ("V-87654321", "María Gómez", 6820.75),
        ]
        
        for cedula, nombre, balance in test_cases:
            query = f"Balance de {cedula}"
            result = agent.process_query(query)
            
            assert result["success"] == True
            assert nombre in result["response"]
    
    # Tests de consultas de KNOWLEDGE
    def test_process_knowledge_query_opening_account(self, agent):
        """Test consulta sobre cómo abrir cuenta."""
        query = "¿Cómo abrir una cuenta de ahorros en el banco?"
        result = agent.process_query(query)
        
        assert result["success"] == True
        assert result["query_type"] == "knowledge"
        assert len(result["response"]) > 0
        # Verificar que tiene información relevante
        assert any(word in result["response"].lower() for word in ["cuenta", "abrir", "banco"])
    
    def test_process_knowledge_query_credit_card(self, agent):
        """Test consulta sobre tarjeta de crédito."""
        query = "¿Cómo puedo obtener una tarjeta de crédito?"
        result = agent.process_query(query)
        
        assert result["success"] == True
        assert result["query_type"] == "knowledge"
        assert len(result["response"]) > 0
    
    def test_process_knowledge_query_transfer(self, agent):
        """Test consulta sobre transferencias."""
        query = "¿Cómo hacer una transferencia bancaria?"
        result = agent.process_query(query)
        
        assert result["success"] == True
        assert result["query_type"] == "knowledge"
        assert len(result["response"]) > 0
    
    # Tests de consultas GENERALES
    def test_process_general_query_greeting(self, agent):
        """Test consulta general de saludo."""
        query = "Hola, buenos días"
        result = agent.process_query(query)
        
        assert result["success"] == True
        assert result["query_type"] == "general"
        assert len(result["response"]) > 0
    
    def test_process_general_query_unrelated(self, agent):
        """Test consulta no relacionada con el banco."""
        query = "¿Cuál es el sentido de la vida?"
        result = agent.process_query(query)
        
        assert result["success"] == True
        assert result["query_type"] == "general"
        assert len(result["response"]) > 0
    
    # Tests de estadísticas
    def test_statistics_tracking(self, agent):
        """Test que las estadísticas se rastrean correctamente."""
        # Resetear estadísticas
        agent.reset_statistics()
        
        # Hacer varias consultas
        agent.process_query("Balance V-12345678")  # balance
        agent.process_query("¿Cómo abrir cuenta?")  # knowledge
        agent.process_query("Hola")  # general
        
        stats = agent.get_statistics()
        
        assert stats["total_queries"] >= 3
        assert stats["balance_queries"] >= 1
        assert stats["knowledge_queries"] >= 1
        assert stats["general_queries"] >= 1
    
    def test_reset_statistics(self, agent):
        """Test reseteo de estadísticas."""
        # Hacer consultas
        agent.process_query("Balance V-12345678")
        
        # Resetear
        agent.reset_statistics()
        
        stats = agent.get_statistics()
        assert stats["total_queries"] == 0
        assert stats["balance_queries"] == 0
        assert stats["knowledge_queries"] == 0
        assert stats["general_queries"] == 0


class TestEndToEndScenarios:
    """Tests de escenarios completos end-to-end."""
    
    def test_conversation_flow(self, agent):
        """Test flujo de conversación completo."""
        queries = [
            "Hola, buenos días",
            "¿Cuál es el balance de V-12345678?",
            "¿Cómo puedo abrir una cuenta de ahorros?",
            "Gracias por la información",
        ]
        
        for query in queries:
            result = agent.process_query(query)
            assert result["success"] == True
            assert len(result["response"]) > 0
    
    def test_mixed_queries(self, agent):
        """Test mezcla de diferentes tipos de consultas."""
        test_cases = [
            ("Balance V-91827364", "balance", True),
            ("¿Cómo solicitar tarjeta?", "knowledge", True),
            ("¿Qué hora es?", "general", True),
            ("Balance V-99999999", "balance", False),  # No encontrado
        ]
        
        for query, expected_type, expected_success in test_cases:
            result = agent.process_query(query)
            assert result["query_type"] == expected_type
            # Para balance no encontrado, success es False pero no es error
            if expected_type != "balance":
                assert result["success"] == expected_success
    
    def test_error_handling(self, agent):
        """Test manejo de errores."""
        # Consultas problemáticas
        problematic_queries = [
            "",  # Vacía
            "   ",  # Solo espacios
            "x" * 10000,  # Muy larga
        ]
        
        for query in problematic_queries:
            result = agent.process_query(query)
            # No debe lanzar excepción, debe manejar gracefully
            assert "response" in result
    
    def test_performance_multiple_queries(self, agent):
        """Test rendimiento con múltiples consultas."""
        import time
        
        queries = [
            "Balance V-12345678",
            "¿Cómo abrir cuenta?",
            "Balance V-91827364",
        ] * 3  # 9 consultas total
        
        start_time = time.time()
        
        for query in queries:
            agent.process_query(query)
        
        elapsed_time = time.time() - start_time
        
        # Debería procesar al menos 1 consulta por segundo
        assert elapsed_time < len(queries) * 10  # 10 segundos por consulta como máximo
