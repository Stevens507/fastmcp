"""Herramientas MCP para gestión de citas según requerimientos del documento"""
import os
import requests
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

# URL del backend API
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8002") + "/api/v1"

class AppointmentTool:
    """Herramientas MCP para citas según el documento de requerimientos"""
    
    @staticmethod
    def schedule_appointment(title: str, start_time: str, duration_minutes: int = 60, description: str = "", location: str = "", participants: List[dict] = None) -> dict:
        """
        Programar una nueva cita
        Herramienta MCP según el documento de requerimientos
        """
        if participants is None:
            participants = []
        
        try:
            # Convertir start_time string a datetime
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = start_dt + timedelta(minutes=duration_minutes)
            
            appointment_data = {
                "title": title,
                "description": description,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
                "location": location,
                "participants": participants
            }
            
            response = requests.post(
                f"{BACKEND_URL}/appointments/",
                json=appointment_data,
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al programar cita: {str(e)}"}
        except ValueError as e:
            return {"error": f"Formato de fecha inválido: {str(e)}"}
    
    @staticmethod
    def check_availability(start_time: str, end_time: str) -> dict:
        """
        Verificar disponibilidad de horario
        Herramienta MCP según el documento de requerimientos
        """
        try:
            availability_data = {
                "start_time": start_time,
                "end_time": end_time
            }
            
            response = requests.post(
                f"{BACKEND_URL}/appointments/check-availability",
                json=availability_data,
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al verificar disponibilidad: {str(e)}"}
    
    @staticmethod
    def list_appointments(date: str = None, status: str = None) -> dict:
        """
        Listar citas con filtro de fecha opcional
        Herramienta MCP según el documento de requerimientos
        """
        params = {"user_id": "default-user"}
        
        if date:
            params["date_filter"] = date
        if status:
            params["status"] = status
        
        try:
            response = requests.get(
                f"{BACKEND_URL}/appointments/",
                params=params,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al listar citas: {str(e)}"}
    
    @staticmethod
    def update_appointment(appointment_id: str, **updates) -> dict:
        """
        Actualizar una cita existente
        Herramienta MCP para modificar citas
        """
        # Filtrar campos válidos
        valid_fields = ["title", "description", "start_time", "end_time", "status", "location", "participants"]
        appointment_updates = {k: v for k, v in updates.items() if k in valid_fields and v is not None}
        
        if not appointment_updates:
            return {"error": "No se proporcionaron campos válidos para actualizar"}
        
        try:
            response = requests.put(
                f"{BACKEND_URL}/appointments/{appointment_id}",
                json=appointment_updates,
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al actualizar cita: {str(e)}"}
    
    @staticmethod
    def delete_appointment(appointment_id: str) -> dict:
        """
        Eliminar una cita
        Herramienta MCP para eliminar citas
        """
        try:
            response = requests.delete(
                f"{BACKEND_URL}/appointments/{appointment_id}",
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al eliminar cita: {str(e)}"}
    
    @staticmethod
    def get_appointment(appointment_id: str) -> dict:
        """
        Obtener una cita específica por ID
        Herramienta MCP para consultas detalladas
        """
        try:
            response = requests.get(
                f"{BACKEND_URL}/appointments/{appointment_id}",
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al obtener cita: {str(e)}"}
    
    @staticmethod
    def complete_appointment(appointment_id: str) -> dict:
        """
        Marcar cita como completada
        Herramienta MCP de conveniencia
        """
        try:
            response = requests.post(
                f"{BACKEND_URL}/appointments/{appointment_id}/complete",
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al completar cita: {str(e)}"}
    
    @staticmethod
    def cancel_appointment(appointment_id: str) -> dict:
        """
        Cancelar una cita
        Herramienta MCP de conveniencia
        """
        try:
            response = requests.post(
                f"{BACKEND_URL}/appointments/{appointment_id}/cancel",
                params={"user_id": "default-user"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al cancelar cita: {str(e)}"}

# Instancia global de herramientas de citas
appointment_tools = AppointmentTool()
