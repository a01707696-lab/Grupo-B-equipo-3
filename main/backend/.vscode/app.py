from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Modelo de datos Task (en memoria)
tasks = [
    {"id": 1, "title": "Aprender Flask", "status": "pendiente"},
    {"id": 2, "title": "Conectar frontend con backend", "status": "hecho"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks")
def get_tasks():
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(debug=True)
