"""Herramientas MCP para gestión de tareas según requerimientos del documento"""
import os
import requests
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# URL del backend API
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8002") + "/api/v1"

class TaskTool:
    """Herramientas MCP para tareas según el documento de requerimientos"""
    
    @staticmethod
    def create_task(title: str, description: str = "", due_date: str = None, priority: str = "medium", category: str = "personal", tags: List[str] = None) -> dict:
        """
        Crear una nueva tarea
        Herramienta MCP según el documento de requerimientos
        """
        if tags is None:
            tags = []
        
        task_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "category": category,
            "tags": tags
        }
        
        if due_date:
            task_data["due_date"] = due_date
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/tasks/",
                json=task_data,
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al crear tarea: {str(e)}"}
    
    @staticmethod
    def list_tasks(status: str = None, priority: str = None, category: str = None) -> dict:
        """
        Listar tareas con filtros opcionales
        Herramienta MCP según el documento de requerimientos
        """
        params = {"user_id": "default-user"}
        
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if category:
            params["category"] = category
        
        try:
            response = requests.get(
                f"{BACKEND_URL}/tasks/",
                params=params,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al listar tareas: {str(e)}"}
    
    @staticmethod
    def update_task(task_id: str, **updates) -> dict:
        """
        Actualizar una tarea existente
        Herramienta MCP según el documento de requerimientos
        """
        # Filtrar campos válidos
        valid_fields = ["title", "description", "status", "priority", "due_date", "category", "tags"]
        task_updates = {k: v for k, v in updates.items() if k in valid_fields and v is not None}
        
        if not task_updates:
            return {"error": "No se proporcionaron campos válidos para actualizar"}
        
        try:
            response = requests.put(
                f"{BACKEND_URL}/tasks/{task_id}",
                json=task_updates,
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al actualizar tarea: {str(e)}"}
    
    @staticmethod
    def delete_task(task_id: str) -> dict:
        """
        Eliminar una tarea
        Herramienta MCP según el documento de requerimientos
        """
        try:
            response = requests.delete(
                f"{BACKEND_URL}/tasks/{task_id}",
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al eliminar tarea: {str(e)}"}
    
    @staticmethod
    def get_task(task_id: str) -> dict:
        """
        Obtener una tarea específica por ID
        Herramienta MCP adicional para consultas detalladas
        """
        try:
            response = requests.get(
                f"{BACKEND_URL}/tasks/{task_id}",
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al obtener tarea: {str(e)}"}
    
    @staticmethod
    def complete_task(task_id: str) -> dict:
        """
        Marcar tarea como completada
        Herramienta MCP de conveniencia
        """
        try:
            response = requests.post(
                f"{BACKEND_URL}/tasks/{task_id}/complete",
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al completar tarea: {str(e)}"}

# Instancia global de herramientas de tareas
task_tools = TaskTool()
