"""
Configuración de pytest.
"""
import pytest
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))


def pytest_configure(config):
    """Configuración inicial de pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup del entorno de testing."""
    import logging
    
    # Configurar logging para tests
    logging.basicConfig(
        level=logging.WARNING,  # Solo warnings y errores durante tests
        format='%(levelname)s - %(name)s - %(message)s'
    )
    
    yield
    
    # Cleanup después de todos los tests
    pass
