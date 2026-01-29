from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 🔑 Permite conexión frontend-backend

# --------------------
# Persistencia en memoria
# --------------------
tasks = [
    {"id": 1, "title": "Primera tarea", "status": "backlog"}
]
next_id = 2

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

    # Validación básica
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
# Arranque del servidor
# --------------------
if __name__ == "__main__":
    app.run(debug=True, port=8000)
