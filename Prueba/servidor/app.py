from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

FILE = "tasks.json"


# ---------- Persistencia ----------
def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


# ---------- Endpoints ----------
@app.route("/", methods=["GET"])
def home():
    return {"message": "Backend funcionando correctamente"}


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())


@app.route("/tasks", methods=["POST"])
def create_task():
    tasks = load_tasks()
    data = request.json

    if not data.get("title"):
        return {"error": "El título es obligatorio"}, 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "status": "backlog",
        "duration": int(data.get("duration", 0))
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    data = request.json

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = data.get("status", task["status"])
            task["duration"] = int(data.get("duration", task["duration"]))
            save_tasks(tasks)
            return jsonify(task)

    return {"error": "Tarea no encontrada"}, 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
