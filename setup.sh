#!/bin/bash

# Script de Inicio Rápido - Sistema de Atención al Cliente
# BANCO HENRY

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║    🏦  BANCO HENRY - Script de Configuración Inicial     ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
echo "🔍 Verificando instalación de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python encontrado: $PYTHON_VERSION"
else
    echo "✗ Python no encontrado. Por favor instala Python 3.10 o superior"
    echo "  Descarga desde: https://www.python.org/downloads/"
    exit 1
fi

echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "✓ Entorno virtual ya existe"
else
    python3 -m venv venv
    echo "✓ Entorno virtual creado"
fi

echo ""

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate
echo "✓ Entorno virtual activado"

echo ""

# Instalar dependencias
echo "📚 Instalando dependencias..."
echo "⏳ Esto puede tardar varios minutos..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas correctamente"
else
    echo "✗ Error al instalar dependencias"
    exit 1
fi

echo ""

# Verificar archivo .env
echo "🔑 Verificando configuración..."
if [ -f ".env" ]; then
    echo "✓ Archivo .env encontrado"
    
    # Verificar si tiene API key
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo "✓ API key de OpenAI configurada"
    else
        echo "⚠ API key de OpenAI no configurada o incompleta"
        echo "  Por favor edita el archivo .env y agrega tu API key"
    fi
else
    echo "⚠ Archivo .env no encontrado"
    echo "  Creando desde template..."
    
    if [ -f ".env.template" ]; then
        cp .env.template .env
        echo "✓ Archivo .env creado"
        echo "  ⚠ IMPORTANTE: Edita el archivo .env y agrega tu API key de OpenAI"
    else
        echo "✗ Template .env.template no encontrado"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✅ Configuración completada!"
echo ""
echo "📝 Próximos pasos:"
echo ""
echo "1. Configura tu API key de OpenAI (si no lo has hecho):"
echo "   nano .env"
echo ""
echo "2. Ejecuta la aplicación CLI:"
echo "   python src/main.py"
echo ""
echo "3. O ejecuta la aplicación Web:"
echo "   streamlit run src/app.py"
echo ""
echo "4. Para ejecutar los tests:"
echo "   pytest"
echo ""
echo "📚 Documentación:"
echo "   - Guía de usuario: docs/USER_GUIDE.md"
echo "   - Arquitectura: docs/ARCHITECTURE.md"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Preguntar si quiere ejecutar la aplicación
read -p "¿Deseas ejecutar la aplicación ahora? (s/n): " ejecutar
if [ "$ejecutar" = "s" ] || [ "$ejecutar" = "S" ]; then
    echo ""
    echo "🚀 Iniciando aplicación..."
    echo ""
    python src/main.py
fi
