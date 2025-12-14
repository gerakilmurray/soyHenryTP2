# Tarea: Sistema de Atención al Cliente Automatizado con LangChain

## 📑 **Tabla de Contenidos**

1. [Objetivo](#objetivo)
2. [Requerimientos](#requerimientos)
3. [Implementación Sugerida](#implementación-sugerida)
4. [Archivos y Directorios](#archivos-y-directorios)
5. [Flexibilidad del Lenguaje de Programación](#flexibilidad-del-lenguaje-de-programación)
6. [Descripción de la Solución Proporcionada](#descripción-de-la-solución-proporcionada)
7. [Ejecución y Gestión de la Solución Proporcionada](#ejecución-y-gestión-de-la-solución-proporcionada)
8. [Entrega del proyecto](#entrega-del-proyecto)

---

## Objetivo

Desarrollar una aplicación utilizando LangChain que sea capaz de procesar solicitudes de clientes y decidir el método más apropiado para responder, ya sea consultando una base de datos, una base de conocimientos, o utilizando el conocimiento integrado en un modelo de lenguaje de gran escala (LLM).

## Requerimientos

El sistema debe ser capaz de identificar y enrutar las solicitudes a uno de los siguientes flujos de trabajo:

1. **Consulta de Balance de Cuentas:** Extraer información de un archivo CSV basado en un ID específico proporcionado por el usuario.

2. **Información General sobre Procesos Bancarios:** Recuperar y generar respuestas a partir de una base de conocimientos sobre procedimientos bancarios específicos como abrir cuentas o realizar transferencias.

3. **Respuestas Generales:** Utilizar el conocimiento del LLM para responder preguntas generales que no requieren consulta de datos externos.

## Implementación Sugerida

- **Indexación de la Base de Conocimientos:** Utilizar el modelo `sentence-transformers/all-MiniLM-L6-v2` para generar embeddings de la base de conocimientos, que luego pueden ser indexados utilizando FAISS. Esta indexación permite realizar búsquedas eficientes y relevantes dentro de la base de conocimientos para responder consultas específicas.

- **Almacenamiento de Vectores:** Se recomienda almacenar la base de datos de vectores localmente y cargarla mediante FAISS para facilitar el acceso rápido y eficiente durante las consultas de recuperación.

- **LangChain:** Utilizar LangChain para integrar y coordinar las diferentes herramientas y modelos, incluyendo el manejo del modelo de lenguaje, la configuración del retriever, y la ejecución de consultas a la base de datos.

## Archivos y Directorios

- **`knowledge_base/`:** Debe contener archivos con información detallada sobre diversos procesos bancarios.
- **`data/saldos.csv`:** Archivo CSV que almacena los balances de cuentas asociados con IDs de cédula específicos.

## Flexibilidad del Lenguaje de Programación

Este proyecto puede ser implementado utilizando JavaScript o Python, según la preferencia del desarrollador. Ambos lenguajes son adecuados para trabajar con LangChain y las herramientas asociadas, y la elección puede depender de la familiaridad del desarrollador con el lenguaje o de requisitos específicos del entorno de ejecución.

## **Descripción de la Solución Proporcionada**

Como referencia para este proyecto, se ha proporcionado una **solución completa implementada en Python** ubicada en el directorio `/solution`. Esta implementación incluye:

### **Componentes Principales:**
- **`main.py`:** Aplicación principal que integra todos los componentes usando LangChain
- **`indexer.py`:** Script para crear y actualizar la base de conocimientos vectorial usando FAISS
- **`data/saldos.csv`:** Base de datos CSV con información de balances de cuenta
- **`knowledge_base/`:** Documentos con información bancaria para el sistema RAG
- **`Dockerfile` y `docker-compose.yml`:** Configuración para ejecución containerizada

### **Tecnologías Utilizadas:**
- **LangChain:** Framework principal para orquestación de componentes
- **OpenAI GPT:** Modelo de lenguaje para procesamiento y generación
- **FAISS:** Base de datos vectorial para búsqueda semántica
- **Sentence Transformers:** Modelo para generación de embeddings
- **Pandas:** Procesamiento de datos CSV
- **Docker:** Containerización multiplataforma

### **Funcionalidades Implementadas:**
1. **Router inteligente** que clasifica las consultas automáticamente
2. **Búsqueda en CSV** por ID de cédula para consultas de balance
3. **Sistema RAG** para información bancaria usando base de conocimientos vectorial
4. **Respuestas generales** usando el conocimiento del LLM
5. **Interfaz de línea de comandos** interactiva
6. **Logging detallado** para debugging y monitoreo

## **Ejecución y Gestión de la Solución Proporcionada**

La solución ha sido **completamente containerizada** para garantizar compatibilidad multiplataforma (Mac/Windows/Linux) y facilitar el despliegue.

### **Ejecución con Docker (Recomendado)**

#### **Prerrequisitos: Instalación de Docker**

Para usar la ejecución con Docker, primero necesitas instalar Docker en tu sistema. Sigue los pasos según tu sistema operativo:

##### **Windows**
1. Visita la página oficial de Docker: https://www.docker.com/products/docker-desktop/
2. Descarga Docker Desktop para Windows
3. Ejecuta el instalador descargado (.exe)
4. Sigue las instrucciones del asistente de instalación
5. Reinicia tu computadora si es necesario
6. Abre Docker Desktop y espera a que se inicie completamente
7. Verifica la instalación abriendo una terminal y ejecutando:
   ```bash
   docker --version
   docker compose --version
   ```

##### **macOS**
1. Visita la página oficial de Docker: https://www.docker.com/products/docker-desktop/
2. Descarga Docker Desktop para Mac (disponible para chips Intel y Apple Silicon)
3. Abre el archivo .dmg descargado
4. Arrastra Docker.app a la carpeta Applications
5. Ejecuta Docker desde Applications
6. Sigue las instrucciones de configuración inicial
7. Verifica la instalación abriendo una terminal y ejecutando:
   ```bash
   docker --version
   docker compose --version
   ```

##### **Linux (Ubuntu/Debian)**
1. Actualiza los paquetes existentes:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```
2. Instala los paquetes necesarios:
   ```bash
   sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release
   ```
3. Agrega la clave GPG oficial de Docker:
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```
4. Agrega el repositorio de Docker:
   ```bash
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
5. Actualiza el índice de paquetes e instala Docker:
   ```bash
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```
6. Agrega tu usuario al grupo docker (opcional, para evitar usar sudo):
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```
7. Verifica la instalación:
   ```bash
   docker --version
   docker compose --version
   ```

##### **Linux (CentOS/RHEL/Fedora)**
1. Actualiza los paquetes existentes:
   ```bash
   sudo yum update -y
   # o para Fedora: sudo dnf update -y
   ```
2. Instala los paquetes necesarios:
   ```bash
   sudo yum install -y yum-utils device-mapper-persistent-data lvm2
   # o para Fedora: sudo dnf install -y dnf-utils device-mapper-persistent-data lvm2
   ```
3. Agrega el repositorio de Docker:
   ```bash
   sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   # o para Fedora: sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
   ```
4. Instala Docker:
   ```bash
   sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
   # o para Fedora: sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```
5. Inicia y habilita Docker:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```
6. Agrega tu usuario al grupo docker (opcional):
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```
7. Verifica la instalación:
   ```bash
   docker --version
   docker compose --version
   ```

#### **Configuración y Ejecución**

##### 1. **Configurar Variables de Entorno**

**⚠️ Importante:** El archivo `.env` debe estar ubicado en la **raíz del proyecto** para que Docker Compose pueda leerlo correctamente.

```bash
# Copia el archivo de ejemplo a la raíz del proyecto
cp solution/.env.example .env

# Edita el archivo .env en la raíz y agrega tu API key de OpenAI
OPENAI_API_KEY=tu_clave_openai_aquí
```

> **Nota:** Si colocas el archivo `.env` dentro de la carpeta `solution/`, Docker Compose no podrá encontrarlo y la aplicación fallará al intentar acceder a las variables de entorno. Asegúrate de que el archivo `.env` esté en el mismo directorio que el archivo `docker-compose.yml`.

##### 2. **Construir y Ejecutar**

> **Nota sobre el tiempo de construcción:** La primera construcción de la imagen Docker puede tardar entre 5-20 minutos, especialmente en sistemas Windows. Esto es normal debido a la descarga e instalación de todas las dependencias de Python (LangChain, FAISS, Transformers, etc.). Las construcciones posteriores serán mucho más rápidas gracias al cache de Docker.

```bash
# Construir la imagen Docker (puede tardar varios minutos la primera vez)
docker compose build

# Ejecutar la aplicación
docker compose run --rm langchain-bank python main.py
```

##### 3. **Ejecución Interactiva**
```bash
# Para ejecutar en modo interactivo
docker compose run --rm langchain-bank bash

# Dentro del contenedor:
python main.py
```

### **Ejecución Local (Alternativa)**

Si prefieres ejecutar localmente sin Docker:

#### 1. **Instalar Dependencias**
```bash
# Usar el archivo de dependencias mínimas (recomendado)
pip install -r solution/requirements-minimal.txt

# O usar el archivo completo
pip install -r solution/requirements-full.txt
```

#### 2. **Configurar Variables de Entorno**

Para ejecución local, puedes colocar el archivo `.env` en la carpeta `solution/` o usar variables de entorno del sistema:

**Opción A - Archivo .env local en solution/:**
```bash
# Crear archivo .env en la carpeta solution/
cp solution/.env.example solution/.env
# Editar .env con tu API key de OpenAI
```

**Opción B - Usar el archivo .env de la raíz:**
```bash
# Si ya tienes el archivo .env en la raíz (para Docker), puedes usarlo directamente
# La aplicación buscará las variables de entorno en el sistema
export OPENAI_API_KEY="tu_clave_openai_aquí"
```

#### 3. **Ejecutar la Aplicación**
```bash
cd solution
python main.py
```

### **Prueba del Sistema**

Para validar que el sistema funciona correctamente, puedes probar los tres flujos de trabajo principales comentando/descomentando las últimas líneas del script `main.py`, guardando los cambios y volviendo a ejecutar la aplicación (**no es necesario reiniciar el contenedor de Docker si escogiste esta opción**):

#### **1. Consulta de Balance (CSV)**
```bash
# Pregunta: "Cual es el balance de la cuenta de la cedula V-91827364?"
# Debe consultar el archivo data/saldos.csv
```

#### **2. Información Bancaria (Knowledge Base)**
```bash
# Pregunta: "Como abro una cuenta de ahorros en el banco?"
# Debe buscar en la base de conocimientos vectorial
```

#### **3. Respuesta General (LLM)**
```bash
# Pregunta: "Cual es el sentido de la vida?"
# Debe usar el conocimiento del modelo de lenguaje
```

### **Reindexación de la Base de Conocimientos**

Si necesitas actualizar la base de conocimientos:

```bash
# Con Docker
docker compose run --rm langchain-bank python indexer.py

# Local
cd solution
python indexer.py
```

Este script generará un directorio `index` que contiene la base de datos de vectores FAISS. Esto es útil si has realizado cambios en la base de conocimientos y necesitas actualizar los índices para reflejar esos cambios.

## **Entrega del proyecto**

Aunque tienes una solución de referencia disponible, te animamos a que desarrolles tu propia implementación para maximizar tu aprendizaje. Tu entrega debe incluir:

### **Entregables Requeridos:**

1. **Código fuente completo:**
   - Implementación completa del sistema de atención al cliente
   - Código bien documentado y estructurado
   - Manejo adecuado de errores y casos edge

2. **Documentación técnica detallada:**
   - **README.md** con instrucciones de instalación y ejecución
   - **Arquitectura del sistema** y decisiones de diseño
   - **Ejemplos de uso** con casos de prueba específicos
   - **Dependencias** y requisitos del sistema
   - **Troubleshooting** para problemas comunes

3. **Pruebas y validación:**
   - **Casos de prueba** para los tres flujos de trabajo principales
   - **Validación** de la integración con OpenAI API
   - **Pruebas** de la funcionalidad de búsqueda en CSV y base de conocimientos
   - **Documentación** de los resultados de las pruebas

### **Criterios de Evaluación:**

- **Funcionalidad completa** de los tres tipos de consulta
- **Calidad del código** y buenas prácticas
- **Documentación clara** y completa
- **Manejo robusto** de errores y casos especiales
- **Creatividad** en la implementación y mejoras adicionales

## ⚙️ Requerimientos Técnicos de Software

### Opción A — Python (solución de referencia)

- [Python 3.10+](https://www.python.org/downloads/)  
- [pip (incluido con Python)](https://pip.pypa.io/en/stable/installation/)  
- [Virtualenv/venv (creación de entornos)](https://docs.python.org/3/library/venv.html)  
- [LangChain (Python)](https://python.langchain.com/) → `pip install langchain`  
- [OpenAI SDK (Python)](https://pypi.org/project/openai/) → `pip install openai`  
- [FAISS (CPU)](https://pypi.org/project/faiss-cpu/) → `pip install faiss-cpu`  
- [Sentence Transformers](https://www.sbert.net/) → `pip install sentence-transformers`  
- [Pandas](https://pandas.pydata.org/) → `pip install pandas`  
- [python-dotenv](https://pypi.org/project/python-dotenv/) → `pip install python-dotenv`  

---

### Opción B — Docker (ejecución recomendada)

- [Docker Desktop (Windows/macOS)](https://www.docker.com/products/docker-desktop/)  
- [Docker Engine (Linux)](https://docs.docker.com/engine/install/)  
- [Docker Compose](https://docs.docker.com/compose/install/)  

---

### Opción C — JavaScript/Node.js (alternativa)

- [Node.js 18+ (incluye npm)](https://nodejs.org/en/download)  
- [Yarn (opcional)](https://classic.yarnpkg.com/lang/en/docs/install)  
- [LangChain.js](https://js.langchain.com/) → `npm install langchain`  
- [OpenAI SDK (JS)](https://www.npmjs.com/package/openai) → `npm install openai`  
- [axios](https://www.npmjs.com/package/axios) → `npm install axios`  
- [dotenv](https://www.npmjs.com/package/dotenv) → `npm install dotenv`  
- (Opcional) [chalk](https://www.npmjs.com/package/chalk) y [ora](https://www.npmjs.com/package/ora) para CLI  
