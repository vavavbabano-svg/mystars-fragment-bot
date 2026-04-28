import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))

@app.route('/buy', methods=['POST'])
def buy():
    try:
        data = request.get_json(force=True)
        return jsonify({"status": "ok", "received": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
