from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend Flask funcionando 🚀"

if __name__ == "__main__":
    app.run(debug=True)
    

print("Backend Flask funcionando 🚀")
