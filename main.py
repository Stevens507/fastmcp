"""Servidor FastMCP principal según requerimientos del documento"""
import os
import sys
import uvicorn
from fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tools.task_tools import task_tools
from tools.appointment_tools import appointment_tools
from config import (
    MCP_HOST, MCP_PORT, BACKEND_URL, MCP_TRANSPORT, 
    FORCE_HTTP_MODE, CORS_ORIGINS, DEBUG
)

# Crear servidor FastMCP
mcp = FastMCP("Gestor Tareas y Citas MCP")

# === HERRAMIENTAS MCP PARA TAREAS ===
@mcp.tool
def create_task(title: str, description: str = "", due_date: str = None, priority: str = "medium", category: str = "personal", tags: list = None) -> dict:
    """
    Crear una nueva tarea
    
    Args:
        title: Título de la tarea (requerido)
        description: Descripción opcional de la tarea
        due_date: Fecha límite en formato ISO (opcional)
        priority: Prioridad (low, medium, high, urgent)
        category: Categoría de la tarea
        tags: Lista de etiquetas
    
    Returns:
        dict: Datos de la tarea creada o error
    """
    return task_tools.create_task(title, description, due_date, priority, category, tags or [])

@mcp.tool
def list_tasks(status: str = None, priority: str = None, category: str = None) -> dict:
    """
    Listar tareas con filtros opcionales
    
    Args:
        status: Filtrar por estado (pending, in_progress, completed, cancelled)
        priority: Filtrar por prioridad (low, medium, high, urgent)
        category: Filtrar por categoría
    
    Returns:
        dict: Lista de tareas que coinciden con los filtros
    """
    return task_tools.list_tasks(status, priority, category)

@mcp.tool
def update_task(task_id: str, title: str = None, description: str = None, status: str = None, priority: str = None, category: str = None, due_date: str = None) -> dict:
    """
    Actualizar una tarea existente
    
    Args:
        task_id: ID de la tarea a actualizar
        title: Nuevo título (opcional)
        description: Nueva descripción (opcional)
        status: Nuevo estado (opcional)
        priority: Nueva prioridad (opcional)
        category: Nueva categoría (opcional)
        due_date: Nueva fecha límite (opcional)
    
    Returns:
        dict: Datos de la tarea actualizada o error
    """
    updates = {}
    if title is not None:
        updates["title"] = title
    if description is not None:
        updates["description"] = description
    if status is not None:
        updates["status"] = status
    if priority is not None:
        updates["priority"] = priority
    if category is not None:
        updates["category"] = category
    if due_date is not None:
        updates["due_date"] = due_date
    
    return task_tools.update_task(task_id, **updates)

@mcp.tool
def delete_task(task_id: str) -> dict:
    """
    Eliminar una tarea
    
    Args:
        task_id: ID de la tarea a eliminar
    
    Returns:
        dict: Confirmación de eliminación o error
    """
    return task_tools.delete_task(task_id)

@mcp.tool
def complete_task(task_id: str) -> dict:
    """
    Marcar tarea como completada
    
    Args:
        task_id: ID de la tarea a completar
    
    Returns:
        dict: Datos de la tarea completada o error
    """
    return task_tools.complete_task(task_id)

# === HERRAMIENTAS MCP PARA CITAS ===
@mcp.tool
def schedule_appointment(title: str, start_time: str, duration_minutes: int = 60, description: str = "", location: str = "", participants: list = None) -> dict:
    """
    Programar una nueva cita
    
    Args:
        title: Título de la cita (requerido)
        start_time: Hora de inicio en formato ISO
        duration_minutes: Duración en minutos (default: 60)
        description: Descripción opcional
        location: Ubicación de la cita
        participants: Lista de participantes con email y status
    
    Returns:
        dict: Datos de la cita creada o error
    """
    return appointment_tools.schedule_appointment(title, start_time, duration_minutes, description, location, participants or [])

@mcp.tool
def check_availability(start_time: str, end_time: str) -> dict:
    """
    Verificar disponibilidad de horario
    
    Args:
        start_time: Hora de inicio en formato ISO
        end_time: Hora de fin en formato ISO
    
    Returns:
        dict: Información sobre disponibilidad y conflictos
    """
    return appointment_tools.check_availability(start_time, end_time)

@mcp.tool
def list_appointments(date: str = None, status: str = None) -> dict:
    """
    Listar citas con filtro de fecha opcional
    
    Args:
        date: Filtrar por fecha específica (YYYY-MM-DD)
        status: Filtrar por estado (scheduled, completed, cancelled, missed)
    
    Returns:
        dict: Lista de citas que coinciden con los filtros
    """
    return appointment_tools.list_appointments(date, status)

@mcp.tool
def update_appointment(appointment_id: str, title: str = None, start_time: str = None, end_time: str = None, description: str = None, location: str = None, status: str = None) -> dict:
    """
    Actualizar una cita existente
    
    Args:
        appointment_id: ID de la cita a actualizar
        title: Nuevo título (opcional)
        start_time: Nueva hora de inicio (opcional)
        end_time: Nueva hora de fin (opcional)
        description: Nueva descripción (opcional)
        location: Nueva ubicación (opcional)
        status: Nuevo estado (opcional)
    
    Returns:
        dict: Datos de la cita actualizada o error
    """
    updates = {}
    if title is not None:
        updates["title"] = title
    if start_time is not None:
        updates["start_time"] = start_time
    if end_time is not None:
        updates["end_time"] = end_time
    if description is not None:
        updates["description"] = description
    if location is not None:
        updates["location"] = location
    if status is not None:
        updates["status"] = status
    
    return appointment_tools.update_appointment(appointment_id, **updates)

@mcp.tool
def cancel_appointment(appointment_id: str) -> dict:
    """
    Cancelar una cita
    
    Args:
        appointment_id: ID de la cita a cancelar
    
    Returns:
        dict: Confirmación de cancelación o error
    """
    return appointment_tools.cancel_appointment(appointment_id)

# === HERRAMIENTAS DE INFORMACIÓN ===
@mcp.tool
def get_task_summary() -> dict:
    """
    Obtener resumen de tareas
    
    Returns:
        dict: Estadísticas generales de tareas
    """
    try:
        all_tasks = task_tools.list_tasks()
        if "error" in all_tasks:
            return all_tasks
        
        tasks = all_tasks.get("tasks", [])
        total = len(tasks)
        
        by_status = {}
        by_priority = {}
        
        for task in tasks:
            status = task.get("status", "unknown")
            priority = task.get("priority", "unknown")
            
            by_status[status] = by_status.get(status, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        return {
            "total_tasks": total,
            "by_status": by_status,
            "by_priority": by_priority
        }
    except Exception as e:
        return {"error": f"Error al obtener resumen: {str(e)}"}

@mcp.tool
def get_appointment_summary() -> dict:
    """
    Obtener resumen de citas
    
    Returns:
        dict: Estadísticas generales de citas
    """
    try:
        all_appointments = appointment_tools.list_appointments()
        if "error" in all_appointments:
            return all_appointments
        
        appointments = all_appointments.get("appointments", [])
        total = len(appointments)
        
        by_status = {}
        
        for apt in appointments:
            status = apt.get("status", "unknown")
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total_appointments": total,
            "by_status": by_status
        }
    except Exception as e:
        return {"error": f"Error al obtener resumen: {str(e)}"}

@mcp.tool
def get_all_data() -> dict:
    """Obtener todos los datos de tareas y citas"""
    try:
        tasks = task_tools.list_tasks()
        appointments = appointment_tools.list_appointments()
        
        return {
            "tasks": tasks,
            "appointments": appointments,
            "timestamp": "2024-01-01T10:00:00Z"
        }
    except Exception as e:
        return {"error": f"Error al obtener datos: {str(e)}"}

if __name__ == "__main__":
    # Verificar si se fuerza el modo HTTP (para Docker Compose)
    force_http = FORCE_HTTP_MODE
    transport_env = MCP_TRANSPORT
    
    # Detectar si estamos siendo ejecutados por Cursor/MCP (stdin no es TTY) o si MCP_TRANSPORT=stdio
    if transport_env == "stdio" or (not force_http and not sys.argv[1:] and not sys.stdin.isatty()):
        # Modo stdio para MCP clients como Cursor - sin prints para no interferir
        mcp.run()
    else:
        print(f"🚀 Iniciando servidor FastMCP")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print("📋 Servidor MCP con herramientas de tareas y citas")
        
        transport = MCP_TRANSPORT
        
        if transport == "http":
            # Pequeño wrapper HTTP compatible con /health y /tools
            http_app = FastAPI(title="FastMCP HTTP Wrapper")
            http_app.add_middleware(
                CORSMiddleware,
                allow_origins=CORS_ORIGINS,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            # Mapa de herramientas HTTP → funciones MCP
            # Wrappers HTTP directos a las implementaciones internas (evita llamar a FunctionTool)
            def _get_task_summary_http():
                data = task_tools.list_tasks()
                if "error" in data:
                    return data
                tasks = data.get("tasks", [])
                by_status = {}
                by_priority = {}
                for t in tasks:
                    by_status[t.get("status", "unknown")] = by_status.get(t.get("status", "unknown"), 0) + 1
                    by_priority[t.get("priority", "unknown")] = by_priority.get(t.get("priority", "unknown"), 0) + 1
                return {"total_tasks": len(tasks), "by_status": by_status, "by_priority": by_priority}

            def _get_appointment_summary_http():
                data = appointment_tools.list_appointments()
                if "error" in data:
                    return data
                appointments = data.get("appointments", [])
                by_status = {}
                for a in appointments:
                    by_status[a.get("status", "unknown")] = by_status.get(a.get("status", "unknown"), 0) + 1
                return {"total_appointments": len(appointments), "by_status": by_status}

            def _get_all_data_http():
                return {"tasks": task_tools.list_tasks(), "appointments": appointment_tools.list_appointments()}

            TOOL_MAP = {
                "create_task": lambda **p: task_tools.create_task(**p),
                "list_tasks": lambda **p: task_tools.list_tasks(**p),
                "update_task": lambda **p: task_tools.update_task(**p),
                "delete_task": lambda **p: task_tools.delete_task(**p),
                "complete_task": lambda **p: task_tools.complete_task(**p),
                "schedule_appointment": lambda **p: appointment_tools.schedule_appointment(**p),
                "check_availability": lambda **p: appointment_tools.check_availability(**p),
                "list_appointments": lambda **p: appointment_tools.list_appointments(**p),
                "update_appointment": lambda **p: appointment_tools.update_appointment(**p),
                "cancel_appointment": lambda **p: appointment_tools.cancel_appointment(**p),
                "get_task_summary": lambda **p: _get_task_summary_http(),
                "get_appointment_summary": lambda **p: _get_appointment_summary_http(),
                "get_all_data": lambda **p: _get_all_data_http(),
            }

            @http_app.get("/health")
            async def health():
                return {"status": "healthy", "backend_url": BACKEND_URL}

            @http_app.get("/tools")
            async def list_tools():
                return {"tools": list(TOOL_MAP.keys())}

            @http_app.post("/tools/{tool_name}")
            async def call_tool(tool_name: str, request: Request):
                if tool_name not in TOOL_MAP:
                    return JSONResponse(status_code=404, content={"error": f"Tool '{tool_name}' not found"})
                payload = {}
                try:
                    payload = await request.json()
                except Exception:
                    payload = {}
                try:
                    result = TOOL_MAP[tool_name](**payload)
                    return result
                except TypeError as te:
                    return JSONResponse(status_code=400, content={"error": str(te)})
                except Exception as e:
                    return JSONResponse(status_code=500, content={"error": str(e)})

            # También montamos el app nativo HTTP de FastMCP bajo /mcp para Cursor
            http_app.mount("/mcp", mcp.http_app())

            uvicorn.run(http_app, host=MCP_HOST, port=MCP_PORT)
        else:
            # Modo stdio por defecto
            mcp.run()