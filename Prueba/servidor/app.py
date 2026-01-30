from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"

# ---------- Persistencia ----------
def load_data(filename, default=[]):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- Endpoints de Usuarios ----------
@app.route("/users", methods=["GET"])
def get_users():
    """Obtener todos los usuarios"""
    return jsonify(load_data(USERS_FILE))

@app.route("/users", methods=["POST"])
def create_user():
    """Crear un nuevo usuario"""
    users = load_data(USERS_FILE)
    data = request.json
    
    if not data or not data.get("name"):
        return {"error": "El nombre es obligatorio"}, 400
    
    # Verificar si el usuario ya existe
    if any(user["name"].lower() == data["name"].lower() for user in users):
        return {"error": "El usuario ya existe"}, 400
    
    new_user = {
        "id": len(users) + 1,
        "name": data["name"].strip()
    }
    
    users.append(new_user)
    save_data(USERS_FILE, users)
    return jsonify(new_user), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Actualizar nombre de usuario"""
    users = load_data(USERS_FILE)
    data = request.json
    
    if not data or not data.get("name"):
        return {"error": "El nombre es obligatorio"}, 400
    
    for user in users:
        if user["id"] == user_id:
            # Verificar que el nuevo nombre no exista (excepto para este usuario)
            if any(u["name"].lower() == data["name"].lower() and u["id"] != user_id for u in users):
                return {"error": "Ya existe otro usuario con ese nombre"}, 400
            
            user["name"] = data["name"].strip()
            save_data(USERS_FILE, users)
            return jsonify(user)
    
    return {"error": "Usuario no encontrado"}, 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Eliminar usuario y desasignar sus tareas"""
    users = load_data(USERS_FILE)
    
    # Verificar si el usuario existe
    if not any(user["id"] == user_id for user in users):
        return {"error": "Usuario no encontrado"}, 404
    
    # Eliminar usuario
    users = [user for user in users if user["id"] != user_id]
    save_data(USERS_FILE, users)
    
    # Desasignar este usuario de todas las tareas
    tasks = load_data(TASKS_FILE)
    tasks_updated = False
    for task in tasks:
        if task.get("assigned_to") == user_id:
            task["assigned_to"] = None
            tasks_updated = True
    
    if tasks_updated:
        save_data(TASKS_FILE, tasks)
    
    return {"message": "Usuario eliminado correctamente"}

# ---------- Endpoints de Tareas ----------
@app.route("/", methods=["GET"])
def home():
    return {"message": "Backend funcionando correctamente"}

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Obtener todas las tareas"""
    tasks = load_data(TASKS_FILE)
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    """Crear una nueva tarea"""
    tasks = load_data(TASKS_FILE)
    data = request.json

    if not data or not data.get("title"):
        return {"error": "El título es obligatorio"}, 400

    # Validar que el usuario asignado exista (si se asigna)
    assigned_to = data.get("assigned_to")
    if assigned_to:  # Solo validar si no es None o vacío
        users = load_data(USERS_FILE)
        # Convertir a int si es string
        try:
            assigned_to_int = int(assigned_to)
        except (ValueError, TypeError):
            return {"error": "ID de usuario inválido"}, 400
            
        if not any(user["id"] == assigned_to_int for user in users):
            return {"error": "El usuario asignado no existe"}, 400
    else:
        assigned_to_int = None

    # Contar tareas en doing para validar límite
    doing_count = len([t for t in tasks if t.get("status") == "doing"])
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "status": "backlog",  # Siempre empieza en backlog
        "estimated": int(data.get("estimated", 0)),
        "real_time": 0,
        "assigned_to": assigned_to_int,  # Usar el valor convertido
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    tasks.append(new_task)
    save_data(TASKS_FILE, tasks)
    
    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Actualizar una tarea"""
    tasks = load_data(TASKS_FILE)
    data = request.json
    
    for task in tasks:
        if task["id"] == task_id:
            # Verificar límite de doing
            if data.get("status") == "doing":
                doing_tasks = [t for t in tasks if t.get("status") == "doing" and t["id"] != task_id]
                if len(doing_tasks) >= 4:
                    return {"error": "Límite máximo de 4 tareas en Doing alcanzado"}, 400
            
            # Validar usuario asignado (si se cambia)
            if "assigned_to" in data and data["assigned_to"] is not None:
                users = load_data(USERS_FILE)
                assigned_to = data["assigned_to"]
                try:
                    assigned_to_int = int(assigned_to)
                except (ValueError, TypeError):
                    return {"error": "ID de usuario inválido"}, 400
                    
                if not any(user["id"] == assigned_to_int for user in users):
                    return {"error": "El usuario asignado no existe"}, 400
                else:
                    data["assigned_to"] = assigned_to_int
            
            # Actualizar campos
            if "title" in data:
                task["title"] = data["title"]
            if "status" in data:
                task["status"] = data["status"]
            if "estimated" in data:
                task["estimated"] = int(data["estimated"])
            if "real_time" in data:
                task["real_time"] = int(data["real_time"])
            if "assigned_to" in data:
                task["assigned_to"] = data["assigned_to"]
            
            task["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_data(TASKS_FILE, tasks)
            return jsonify(task)
    
    return {"error": "Tarea no encontrada"}, 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Eliminar una tarea"""
    tasks = load_data(TASKS_FILE)
    
    # Verificar si la tarea existe
    if not any(task["id"] == task_id for task in tasks):
        return {"error": "Tarea no encontrada"}, 404
    
    tasks = [task for task in tasks if task["id"] != task_id]
    save_data(TASKS_FILE, tasks)
    return {"message": "Tarea eliminada"}

@app.route("/stats", methods=["GET"])
def get_stats():
    """Obtener estadísticas del tablero"""
    tasks = load_data(TASKS_FILE)
    
    doing_tasks = [t for t in tasks if t.get("status") == "doing"]
    done_tasks = [t for t in tasks if t.get("status") == "done"]
    
    doing_estimated = sum(t.get("estimated", 0) for t in doing_tasks)
    done_real = sum(t.get("real_time", 0) for t in done_tasks)
    
    return jsonify({
        "total_tasks": len(tasks),
        "doing_count": len(doing_tasks),
        "doing_estimated": doing_estimated,
        "done_count": len(done_tasks),
        "done_real": done_real
    })

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Servidor Kanban iniciado")
    print("👥 Gestión completa de usuarios (CRUD)")
    print("📊 Gestión de tareas con asignación")
    print("🌐 Accede en: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)