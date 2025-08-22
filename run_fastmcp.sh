#!/bin/bash

# Script para ejecutar el FastMCP con configuración .env
echo "🚀 Iniciando FastMCP..."
echo "📁 Directorio: $(pwd)"
echo "🔧 Cargando configuración desde .env"

# Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo "❌ Error: No se encontró el archivo .env"
    echo "📝 Crea el archivo .env con las configuraciones necesarias"
    exit 1
fi

# Mostrar configuración básica
echo "📋 Configuración:"
echo "   - Puerto MCP: $(grep MCP_PORT .env | cut -d'=' -f2)"
echo "   - Host MCP: $(grep MCP_HOST .env | cut -d'=' -f2)"
echo "   - Backend URL: $(grep BACKEND_URL .env | cut -d'=' -f2)"
echo "   - Transport: $(grep MCP_TRANSPORT .env | cut -d'=' -f2)"

# Instalar dependencias si es necesario
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Verificar que el backend esté disponible
BACKEND_URL=$(grep BACKEND_URL .env | cut -d'=' -f2)
echo "🔍 Verificando conexión con backend en $BACKEND_URL..."
if curl -s "$BACKEND_URL/health" > /dev/null; then
    echo "✅ Backend disponible"
else
    echo "⚠️  Warning: No se puede conectar al backend"
    echo "   Asegúrate de que el backend esté corriendo en $BACKEND_URL"
fi

# Ejecutar el FastMCP
echo "🌟 Iniciando FastMCP..."
python main.py
