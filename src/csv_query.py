"""
Módulo para consultas a la base de datos CSV.
Maneja la búsqueda de información de cuentas bancarias.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict
from src.config import CSV_FILE

logger = logging.getLogger(__name__)


class CSVQueryManager:
    """Gestor de consultas a archivos CSV."""

    def __init__(self, csv_path: Path = CSV_FILE):
        """
        Inicializa el gestor de consultas CSV.

        Args:
            csv_path: Ruta al archivo CSV con los datos de cuentas
        """
        self.csv_path = csv_path
        self.df: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self) -> None:
        """Carga el archivo CSV en memoria."""
        try:
            self.df = pd.read_csv(self.csv_path)
            logger.info(f"CSV cargado exitosamente: {len(self.df)} registros")
        except FileNotFoundError:
            logger.error(f"Archivo CSV no encontrado: {self.csv_path}")
            raise
        except Exception as e:
            logger.error(f"Error al cargar CSV: {e}")
            raise

    def get_balance_by_cedula(self, cedula_id: str) -> Dict[str, any]:
        """
        Obtiene el balance de una cuenta por ID de cédula.

        Args:
            cedula_id: ID de cédula del cliente (ej: "V-12345678")

        Returns:
            Diccionario con la información de la cuenta o None si no se encuentra

        Raises:
            ValueError: Si el formato de cédula es inválido
        """
        # Validar formato de cédula
        cedula_id = cedula_id.strip().upper()

        if not cedula_id:
            raise ValueError("ID de cédula no puede estar vacío")

        # Buscar en el DataFrame
        result = self.df[self.df["ID_Cedula"] == cedula_id]

        if result.empty:
            logger.warning(f"Cédula no encontrada: {cedula_id}")
            return {
                "found": False,
                "message": f"No se encontró ninguna cuenta con la cédula {cedula_id}",
            }

        # Extraer datos
        row = result.iloc[0]
        balance_info = {
            "found": True,
            "cedula": row["ID_Cedula"],
            "nombre": row["Nombre"],
            "balance": float(row["Balance"]),
            "message": f"El balance de la cuenta de {row['Nombre']} (Cédula: {row['ID_Cedula']}) es: ${row['Balance']:.2f}",
        }

        logger.info(f"Balance consultado exitosamente para {cedula_id}")
        return balance_info

    def get_all_accounts(self) -> pd.DataFrame:
        """
        Obtiene todas las cuentas disponibles.

        Returns:
            DataFrame con todas las cuentas
        """
        return self.df.copy()

    def search_by_name(self, name: str) -> pd.DataFrame:
        """
        Busca cuentas por nombre (búsqueda parcial).

        Args:
            name: Nombre o parte del nombre a buscar

        Returns:
            DataFrame con los resultados
        """
        name_lower = name.lower()
        results = self.df[
            self.df["Nombre"].str.lower().str.contains(name_lower, na=False)
        ]
        logger.info(f"Búsqueda por nombre '{name}': {len(results)} resultados")
        return results


def format_balance_response(balance_info: Dict[str, any]) -> str:
    """
    Formatea la respuesta de balance para presentación al usuario.

    Args:
        balance_info: Diccionario con información de balance

    Returns:
        String formateado para mostrar al usuario
    """
    if not balance_info["found"]:
        return balance_info["message"]

    return f"""
📊 **Información de Cuenta**
━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Titular: {balance_info['nombre']}
🆔 Cédula: {balance_info['cedula']}
💰 Balance: ${balance_info['balance']:,.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━
"""
