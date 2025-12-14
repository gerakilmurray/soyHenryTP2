# 🚀 INICIO RÁPIDO

## Configuración en 3 Pasos

### 1️⃣ Configurar Entorno

**Windows:**
```powershell
# Ejecutar script de configuración automática
.\setup.ps1
```

**macOS/Linux:**
```bash
# Dar permisos y ejecutar
chmod +x setup.sh
./setup.sh
```

**O manualmente:**
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key

Crear archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=sk-tu-clave-api-aqui
```

**¿Dónde obtener la API key?**
1. Ve a https://platform.openai.com/
2. Crea/inicia sesión
3. Ve a "API Keys"
4. Crea nueva key
5. Copia y pega en el archivo `.env`

### 3️⃣ Ejecutar

**Interfaz CLI:**
```bash
python src/main.py
```

**Interfaz Web:**
```bash
streamlit run src/app.py
```

## ✅ Verificar Instalación

```bash
# Verificar que todo está instalado
python -c "import langchain, streamlit, faiss; print('✓ Todo OK')"

# Ejecutar tests
pytest

# Ver cobertura
pytest --cov=src --cov-report=html
```

## 💡 Primeras Consultas

Una vez iniciada la aplicación, prueba estas consultas:

```
# 1. Balance
¿Cuál es el balance de la cédula V-12345678?

# 2. Información bancaria
¿Cómo abrir una cuenta de ahorros?

# 3. General
Hola, buenos días
```

## 📚 Más Información

- **Guía completa:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Arquitectura:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Informe:** [docs/INFORME_FINAL.md](docs/INFORME_FINAL.md)

## 🆘 Problemas Comunes

### Error: "OPENAI_API_KEY no encontrada"
→ Verifica que el archivo `.env` existe y tiene tu API key

### Error: "Module not found"
→ Activa el entorno virtual y ejecuta `pip install -r requirements.txt`

### Tests fallan
→ Asegúrate de que el archivo `.env` está configurado

## 📞 Ayuda

¿Tienes problemas? Revisa la sección de Troubleshooting en [USER_GUIDE.md](docs/USER_GUIDE.md)
