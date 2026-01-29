from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --------------------
# Persistencia en memoria
# --------------------
tasks = []
next_id = 1

# --------------------
# Endpoint de prueba
# --------------------
@app.route("/")
def home():
    return jsonify({"message": "Backend funcionando correctamente"})

# --------------------
# GET /tasks → listar tareas
# --------------------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

# --------------------
# POST /tasks → crear tarea
# --------------------
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()

    if not data or "title" not in data or data["title"].strip() == "":
        return jsonify({"error": "El título es obligatorio"}), 400

    new_task = {
        "id": next_id,
        "title": data["title"],
        "status": "backlog"
    }

    tasks.append(new_task)
    next_id += 1

    return jsonify(new_task), 201

# --------------------
# PUT /tasks/<id> → cambiar estado
# --------------------
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = data.get("status", task["status"])
            return jsonify(task)

    return jsonify({"error": "Tarea no encontrada"}), 404

# --------------------
# DELETE /tasks/<id> → eliminar tarea
# --------------------
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarea eliminada"})

# --------------------
# Arranque
# --------------------
if __name__ == "__main__":
    app.run(debug=True, port=8000)
