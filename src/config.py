"""
Configuración centralizada del sistema.
"""

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Cargar variables de entorno
_ = load_dotenv(find_dotenv())

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
INDEX_DIR = PROJECT_ROOT / "solution" / "index"

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no encontrada en las variables de entorno")

# Configuración del modelo
LLM_MODEL = "gpt-4-0125-preview"
LLM_TEMPERATURE = 0.7

# Configuración de embeddings
EMBEDDINGS_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Configuración del retriever
RETRIEVER_K = 3  # Número de documentos a recuperar

# Archivo de datos
CSV_FILE = DATA_DIR / "saldos.csv"

# Logging
LOG_LEVEL = "INFO"
