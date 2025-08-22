"""Configuración FastMCP según requerimientos"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración del servidor MCP
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", 8001))
MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "http")

# URL del backend API
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8002")

# Configuración de timeouts
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 5))  # segundos para requests al backend
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", 3))      # segundos para respuestas del agente según requerimientos

# Configuración de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Debug mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Modo HTTP forzado
FORCE_HTTP_MODE = os.getenv("FORCE_HTTP_MODE", "false").lower() == "true"

# Información del servidor
SERVER_NAME = "Gestor Tareas y Citas MCP"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "Servidor MCP para gestión inteligente de tareas y citas"

# Herramientas disponibles según el documento
AVAILABLE_TOOLS = [
    "create_task",
    "list_tasks", 
    "update_task",
    "delete_task",
    "complete_task",
    "schedule_appointment",
    "check_availability",
    "list_appointments",
    "update_appointment",
    "cancel_appointment",
    "get_task_summary",
    "get_appointment_summary"
]

# Recursos disponibles
AVAILABLE_RESOURCES = [
    "tasks_and_appointments"
]