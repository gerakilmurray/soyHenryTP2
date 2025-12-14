# 📖 Guía de Uso del Sistema

## Índice
1. [Instalación](#instalación)
2. [Configuración](#configuración)
3. [Uso de la Interfaz CLI](#uso-de-la-interfaz-cli)
4. [Uso de la Interfaz Web](#uso-de-la-interfaz-web)
5. [Ejecutar Tests](#ejecutar-tests)
6. [Casos de Uso](#casos-de-uso)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Instalación

### Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/soyHenryTP2.git
cd soyHenryTP2
```

### Paso 2: Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración

### 1. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Windows PowerShell
Copy-Item .env.template .env

# macOS/Linux
cp .env.template .env
```

Edita el archivo `.env` y agrega tu API key de OpenAI:

```env
OPENAI_API_KEY=sk-tu-clave-api-aqui
```

### 2. Obtener API Key de OpenAI

1. Visita https://platform.openai.com/
2. Crea una cuenta o inicia sesión
3. Ve a **API Keys** en tu perfil
4. Crea una nueva API key
5. Copia la key y pégala en tu archivo `.env`

### 3. Verificar Instalación

```bash
# Verificar que Python puede importar los módulos
python -c "import langchain; print('✓ LangChain instalado')"
python -c "import streamlit; print('✓ Streamlit instalado')"
python -c "import faiss; print('✓ FAISS instalado')"
```

---

## 💻 Uso de la Interfaz CLI

### Modo Interactivo (Recomendado)

```bash
python src/main.py
```

**Pantalla de inicio:**
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🏦  BANCO HENRY - Sistema de Atención             ║
║                  al Cliente Automatizado                  ║
║                                                           ║
║        Powered by LangChain & OpenAI GPT-4               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Consultas de Ejemplo

#### 1. Consultar Balance
```
🙋 Tu consulta: ¿Cuál es el balance de la cédula V-12345678?

💰 Tipo de consulta: BALANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Información de Cuenta**
━━━━━━━━━━━━━━━━━━━━━━━━
👤 Titular: Juan Pérez
🆔 Cédula: V-12345678
💰 Balance: $1,250.50
━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 2. Información Bancaria
```
🙋 Tu consulta: ¿Cómo abrir una cuenta de ahorros?

📚 Tipo de consulta: KNOWLEDGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para abrir una cuenta en BANCO HENRY, sigue estos pasos:
1. Visita la página web...
2. Elige el tipo de cuenta...
[...]
```

#### 3. Pregunta General
```
🙋 Tu consulta: Hola, buenos días

💬 Tipo de consulta: GENERAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¡Buenos días! Bienvenido a BANCO HENRY. Soy tu asistente virtual...
```

### Comandos del Sistema

| Comando | Descripción |
|---------|-------------|
| `/help` | Muestra el menú de ayuda |
| `/stats` | Muestra estadísticas de uso |
| `/clear` | Limpia la pantalla |
| `/exit` o `/quit` | Salir del sistema |

#### Ver Estadísticas
```
🙋 Tu consulta: /stats

📊 ESTADÍSTICAS DEL SISTEMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total de consultas procesadas: 15

Desglose por tipo:
  💰 Consultas de balance:        5
  📚 Consultas de base de conocimiento: 7
  💬 Consultas generales:         3

Tasa de éxito: 100.0%
```

### Modo Consulta Única

Para hacer una sola consulta sin entrar al modo interactivo:

```bash
python src/main.py --query "Balance V-12345678"
```

### Modo Batch

Para procesar múltiples consultas desde un archivo:

1. Crea un archivo `consultas.txt`:
```text
Balance V-12345678
¿Cómo abrir una cuenta?
Balance V-91827364
¿Cómo solicitar tarjeta de crédito?
```

2. Ejecuta en modo batch:
```bash
python src/main.py --batch consultas.txt
```

### Modo Verbose (Debugging)

Para ver logs detallados:

```bash
python src/main.py --verbose
```

---

## 🌐 Uso de la Interfaz Web

### Iniciar la Aplicación Web

```bash
streamlit run src/app.py
```

Automáticamente se abrirá en tu navegador: `http://localhost:8501`

### Características de la Interfaz Web

#### 1. **Área Principal**
- Campo de texto para escribir consultas
- Botón "Consultar" para enviar
- Botón "Limpiar" para resetear historial

#### 2. **Barra Lateral**
- **Acerca del Sistema:** Información general
- **Ejemplos de Consultas:** Casos de uso
- **Estadísticas:** Métricas en tiempo real
- **Tecnologías:** Stack tecnológico

#### 3. **Historial**
- Últimas 10 consultas
- Expandible para ver detalles
- Persistente durante la sesión

#### 4. **Visualización de Respuestas**

**Balance:**
```
💰 Respuesta (BALANCE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Información formateada con métricas]

Titular | Cédula | Balance
```

**Knowledge:**
```
📚 Respuesta (KNOWLEDGE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Respuesta del sistema]

📄 Ver fuentes de información ▼
  Fuente 1: nueva_cuenta.txt
  [Contenido...]
```

### Configuración de Streamlit

Puedes personalizar la configuración creando `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = false
```

---

## 🧪 Ejecutar Tests

### Ejecutar Todos los Tests

```bash
pytest
```

### Tests con Cobertura

```bash
pytest --cov=src --cov-report=html
```

Luego abre `htmlcov/index.html` en tu navegador para ver el reporte.

### Ejecutar Tests Específicos

```bash
# Un archivo
pytest tests/test_csv_query.py

# Una clase
pytest tests/test_csv_query.py::TestCSVQueryManager

# Un test específico
pytest tests/test_csv_query.py::TestCSVQueryManager::test_get_balance_existing_cedula
```

### Tests por Categoría

```bash
# Solo tests de integración
pytest -m integration

# Excluir tests lentos
pytest -m "not slow"
```

### Modo Verbose

```bash
pytest -v
```

### Detener en el Primer Fallo

```bash
pytest -x
```

---

## 💡 Casos de Uso

### Caso 1: Cliente Consulta Su Balance

**Contexto:** Un cliente quiere saber cuánto dinero tiene en su cuenta.

**Interacción:**
```
Cliente: "Hola, quisiera saber mi balance. Mi cédula es V-12345678"

Sistema: 
  - Clasifica como: BALANCE
  - Extrae cédula: V-12345678
  - Consulta CSV
  - Responde con información formateada

📊 **Información de Cuenta**
👤 Titular: Juan Pérez
🆔 Cédula: V-12345678
💰 Balance: $1,250.50
```

### Caso 2: Cliente Pregunta Cómo Abrir Cuenta

**Contexto:** Un cliente potencial quiere abrir una cuenta nueva.

**Interacción:**
```
Cliente: "¿Cómo puedo abrir una cuenta de ahorros?"

Sistema:
  - Clasifica como: KNOWLEDGE
  - Busca en base de conocimientos
  - Encuentra documento relevante
  - Genera respuesta contextualizada con LLM

Para abrir una cuenta en BANCO HENRY:
1. Visita nuestra página web...
2. Completa el formulario...
[...]
```

### Caso 3: Conversación Natural

**Contexto:** Cliente tiene una conversación fluida.

**Interacción:**
```
Cliente: "Hola, buenos días"
Sistema: [Respuesta amigable de saludo]

Cliente: "Quiero saber mi balance"
Sistema: "Por favor proporciona tu número de cédula"

Cliente: "V-12345678"
Sistema: [Información de balance]

Cliente: "Gracias"
Sistema: [Despedida cordial]
```

### Caso 4: Múltiples Consultas en Batch

**Contexto:** Análisis de múltiples cuentas.

**Archivo `cuentas.txt`:**
```
Balance V-12345678
Balance V-87654321
Balance V-91827364
```

**Comando:**
```bash
python src/main.py --batch cuentas.txt
```

**Resultado:** Reporte con todos los balances.

---

## 🔧 Troubleshooting

### Problema 1: Error de API Key

**Síntoma:**
```
Error: OPENAI_API_KEY no encontrada en las variables de entorno
```

**Solución:**
1. Verifica que existe el archivo `.env`
2. Verifica que contiene `OPENAI_API_KEY=sk-...`
3. Reinicia el terminal
4. Reactiva el entorno virtual

### Problema 2: Módulos No Encontrados

**Síntoma:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Solución:**
```bash
# Verifica que el entorno virtual está activado
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Reinstala dependencias
pip install -r requirements.txt
```

### Problema 3: FAISS No Se Instala

**Síntoma:**
```
ERROR: Could not build wheels for faiss-cpu
```

**Solución (Windows):**
```bash
# Instalar Visual C++ Build Tools
# Descargar de: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# O usar conda
conda install -c conda-forge faiss-cpu
```

**Solución (macOS):**
```bash
# Usar conda
conda install -c conda-forge faiss-cpu
```

### Problema 4: Índice FAISS No Encontrado

**Síntoma:**
```
Índice no encontrado en solution/index
```

**Solución:**
```bash
# Crear el índice manualmente
cd solution
python indexer.py
```

### Problema 5: Error de Permisos en CSV

**Síntoma:**
```
PermissionError: [Errno 13] Permission denied: 'data/saldos.csv'
```

**Solución:**
1. Cierra cualquier programa que tenga abierto el CSV (Excel, etc.)
2. Verifica permisos del archivo
3. Ejecuta como administrador si es necesario

### Problema 6: Streamlit No Abre el Navegador

**Síntoma:**
La aplicación inicia pero no abre el navegador.

**Solución:**
```bash
# Abre manualmente
http://localhost:8501

# O especifica el puerto
streamlit run src/app.py --server.port 8502
```

### Problema 7: Timeout en Consultas

**Síntoma:**
Las consultas tardan demasiado o dan timeout.

**Solución:**
1. Verifica tu conexión a internet
2. Verifica el estado de la API de OpenAI
3. Reduce la temperatura o el modelo:
   ```env
   LLM_MODEL=gpt-3.5-turbo
   ```

### Problema 8: Tests Fallan

**Síntoma:**
```
FAILED tests/test_integration.py
```

**Solución:**
```bash
# Ejecuta en modo verbose para ver el error
pytest -v

# Verifica que el .env está configurado
cat .env  # Linux/Mac
type .env  # Windows

# Ejecuta solo tests unitarios (más rápidos)
pytest tests/test_csv_query.py
```

---

## 📞 Soporte

### Recursos
- **Documentación:** `docs/`
- **Arquitectura:** `docs/ARCHITECTURE.md`
- **API Reference:** Docstrings en el código

### Reportar Problemas
1. Verifica la sección de Troubleshooting
2. Revisa los logs en `customer_service.log`
3. Crea un issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Logs relevantes
   - Sistema operativo y versión de Python

### Contribuir
1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crea un Pull Request

---

## 🎓 Recursos de Aprendizaje

### LangChain
- [Documentación Oficial](https://python.langchain.com/)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Retrieval QA](https://python.langchain.com/docs/use_cases/question_answering/)

### FAISS
- [Documentación](https://faiss.ai/)
- [Tutorial](https://www.pinecone.io/learn/faiss/)

### OpenAI
- [API Documentation](https://platform.openai.com/docs/)
- [Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

### Streamlit
- [Docs](https://docs.streamlit.io/)
- [Gallery](https://streamlit.io/gallery)
