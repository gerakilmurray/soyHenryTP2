# Script de Inicio Rápido - Sistema de Atención al Cliente
# BANCO HENRY

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                           ║" -ForegroundColor Cyan
Write-Host "║    🏦  BANCO HENRY - Script de Configuración Inicial     ║" -ForegroundColor Cyan
Write-Host "║                                                           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "🔍 Verificando instalación de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python no encontrado. Por favor instala Python 3.10 o superior" -ForegroundColor Red
    Write-Host "  Descarga desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Verificar versión de Python
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Host "✗ Se requiere Python 3.10 o superior (encontrado: $pythonVersion)" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Crear entorno virtual
Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Entorno virtual ya existe" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
}

Write-Host ""

# Activar entorno virtual
Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Entorno virtual activado" -ForegroundColor Green

Write-Host ""

# Instalar dependencias
Write-Host "📚 Instalando dependencias..." -ForegroundColor Yellow
Write-Host "⏳ Esto puede tardar varios minutos..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "✗ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verificar archivo .env
Write-Host "🔑 Verificando configuración..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ Archivo .env encontrado" -ForegroundColor Green
    
    # Verificar si tiene API key
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-") {
        Write-Host "✓ API key de OpenAI configurada" -ForegroundColor Green
    } else {
        Write-Host "⚠ API key de OpenAI no configurada o incompleta" -ForegroundColor Yellow
        Write-Host "  Por favor edita el archivo .env y agrega tu API key" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Archivo .env no encontrado" -ForegroundColor Yellow
    Write-Host "  Creando desde template..." -ForegroundColor Cyan
    
    if (Test-Path ".env.template") {
        Copy-Item ".env.template" ".env"
        Write-Host "✓ Archivo .env creado" -ForegroundColor Green
        Write-Host "  ⚠ IMPORTANTE: Edita el archivo .env y agrega tu API key de OpenAI" -ForegroundColor Yellow
    } else {
        Write-Host "✗ Template .env.template no encontrado" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configura tu API key de OpenAI (si no lo has hecho):" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Ejecuta la aplicación CLI:" -ForegroundColor White
Write-Host "   python src/main.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. O ejecuta la aplicación Web:" -ForegroundColor White
Write-Host "   streamlit run src/app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Para ejecutar los tests:" -ForegroundColor White
Write-Host "   pytest" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentación:" -ForegroundColor Yellow
Write-Host "   - Guía de usuario: docs/USER_GUIDE.md" -ForegroundColor White
Write-Host "   - Arquitectura: docs/ARCHITECTURE.md" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Preguntar si quiere ejecutar la aplicación
$ejecutar = Read-Host "¿Deseas ejecutar la aplicación ahora? (s/n)"
if ($ejecutar -eq "s" -or $ejecutar -eq "S") {
    Write-Host ""
    Write-Host "🚀 Iniciando aplicación..." -ForegroundColor Green
    Write-Host ""
    python src/main.py
}
