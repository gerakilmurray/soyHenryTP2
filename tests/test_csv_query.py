"""
Tests unitarios para el módulo de consultas CSV.
"""
import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.csv_query import CSVQueryManager, format_balance_response


@pytest.fixture
def csv_manager():
    """Fixture para crear una instancia del CSVQueryManager."""
    return CSVQueryManager()


class TestCSVQueryManager:
    """Tests para CSVQueryManager."""
    
    def test_initialization(self, csv_manager):
        """Test que el manager se inicializa correctamente."""
        assert csv_manager.df is not None
        assert isinstance(csv_manager.df, pd.DataFrame)
        assert len(csv_manager.df) > 0
    
    def test_get_balance_existing_cedula(self, csv_manager):
        """Test consulta de balance con cédula existente."""
        result = csv_manager.get_balance_by_cedula("V-12345678")
        
        assert result["found"] == True
        assert result["cedula"] == "V-12345678"
        assert result["nombre"] == "Juan Pérez"
        assert result["balance"] == 1250.5
    
    def test_get_balance_non_existing_cedula(self, csv_manager):
        """Test consulta de balance con cédula no existente."""
        result = csv_manager.get_balance_by_cedula("V-99999999")
        
        assert result["found"] == False
        assert "No se encontró" in result["message"]
    
    def test_get_balance_case_insensitive(self, csv_manager):
        """Test que la búsqueda no distingue mayúsculas/minúsculas."""
        result1 = csv_manager.get_balance_by_cedula("v-12345678")
        result2 = csv_manager.get_balance_by_cedula("V-12345678")
        
        assert result1["found"] == result2["found"]
        assert result1["cedula"] == result2["cedula"]
    
    def test_get_balance_with_whitespace(self, csv_manager):
        """Test que maneja espacios en blanco correctamente."""
        result = csv_manager.get_balance_by_cedula("  V-12345678  ")
        
        assert result["found"] == True
        assert result["cedula"] == "V-12345678"
    
    def test_get_balance_empty_cedula(self, csv_manager):
        """Test con cédula vacía."""
        with pytest.raises(ValueError):
            csv_manager.get_balance_by_cedula("")
    
    def test_get_all_accounts(self, csv_manager):
        """Test obtención de todas las cuentas."""
        accounts = csv_manager.get_all_accounts()
        
        assert isinstance(accounts, pd.DataFrame)
        assert len(accounts) == len(csv_manager.df)
        assert list(accounts.columns) == ["ID_Cedula", "Nombre", "Balance"]
    
    def test_search_by_name(self, csv_manager):
        """Test búsqueda por nombre."""
        results = csv_manager.search_by_name("Juan")
        
        assert len(results) > 0
        assert "Juan" in results.iloc[0]["Nombre"]
    
    def test_search_by_name_partial(self, csv_manager):
        """Test búsqueda parcial por nombre."""
        results = csv_manager.search_by_name("érez")
        
        assert len(results) > 0
        assert "Pérez" in results.iloc[0]["Nombre"]
    
    def test_search_by_name_case_insensitive(self, csv_manager):
        """Test que búsqueda por nombre no distingue mayúsculas."""
        results = csv_manager.search_by_name("JUAN")
        
        assert len(results) > 0


class TestFormatBalanceResponse:
    """Tests para la función de formateo de respuestas."""
    
    def test_format_found_balance(self):
        """Test formateo de balance encontrado."""
        balance_info = {
            "found": True,
            "nombre": "Juan Pérez",
            "cedula": "V-12345678",
            "balance": 1250.50
        }
        
        result = format_balance_response(balance_info)
        
        assert "Juan Pérez" in result
        assert "V-12345678" in result
        assert "1,250.50" in result
    
    def test_format_not_found_balance(self):
        """Test formateo de balance no encontrado."""
        balance_info = {
            "found": False,
            "message": "No se encontró la cédula"
        }
        
        result = format_balance_response(balance_info)
        
        assert "No se encontró" in result


# Tests de integración
class TestCSVIntegration:
    """Tests de integración para el módulo CSV."""
    
    def test_multiple_queries(self, csv_manager):
        """Test múltiples consultas consecutivas."""
        cedulas = ["V-12345678", "V-87654321", "V-99999999"]
        
        for cedula in cedulas:
            result = csv_manager.get_balance_by_cedula(cedula)
            assert "found" in result
    
    def test_data_consistency(self, csv_manager):
        """Test que los datos son consistentes."""
        result = csv_manager.get_balance_by_cedula("V-12345678")
        
        # Verificar que el balance es un número positivo
        assert result["balance"] >= 0
        
        # Verificar que el nombre no está vacío
        assert len(result["nombre"]) > 0
