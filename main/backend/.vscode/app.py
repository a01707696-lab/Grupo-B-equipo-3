from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =========================
# PERSISTENCIA EN MEMORIA
# =========================
tasks = [
    {"id": 1, "title": "Aprender Flask", "status": "pendiente"},
    {"id": 2, "title": "Conectar frontend con backend", "status": "hecho"}
]

next_id = 3  # siguiente ID disponible


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.json

    nueva_tarea = {
        "id": next_id,
        "title": data.get("title"),
        "status": "pendiente"
    }

    tasks.append(nueva_tarea)
    next_id += 1

    return jsonify(nueva_tarea), 201


if __name__ == "__main__":
    app.run(debug=True)

