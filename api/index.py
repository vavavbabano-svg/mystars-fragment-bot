import os
import json
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))

@app.route('/buy', methods=['POST'])
def buy():
    try:
        # Получаем данные от Lava
        data = request.get_json()
        username = data.get('username')
        stars = data.get('stars')
        
        if not username or not stars:
            return jsonify({"error": "Missing username or stars"}), 400
        
        # Покупаем звёзды через отдельный скрипт
        result = subprocess.run(
            ['python', 'buy_stars.py', '--username', username, '--stars', str(stars)],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            return jsonify({"status": "ok", "message": f"Stars sent to {username}"})
        else:
            return jsonify({"error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
