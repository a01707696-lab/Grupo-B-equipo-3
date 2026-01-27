from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"message": "Backend funcionando correctamente"})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
