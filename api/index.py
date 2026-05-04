import os
import json
import re
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))

@app.route('/buy', methods=['POST'])
def buy():
    try:
        data = request.get_json()
        
        username = None
        stars = None
        
        if 'username' in data:
            username = data['username']
            stars = data.get('stars')
        
        if 'custom_fields' in data and data['custom_fields']:
            custom = json.loads(data['custom_fields']) if isinstance(data['custom_fields'], str) else data['custom_fields']
            if not username:
                username = custom.get('username')
            if stars is None:
                stars = custom.get('stars')
        
        if not username or stars is None:
            return jsonify({"error": "Missing username or stars"}), 400
        
        stars = int(stars) if stars else 0
        
        result = subprocess.run(
            ['python', 'buy_stars.py', '--username', username, '--stars', str(stars)],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"Stars purchased: {result.stdout}")
            return jsonify({"status": "ok", "message": f"Stars sent to {username}"}), 200
        else:
            print(f"Error: {result.stderr}")
            return jsonify({"error": result.stderr}), 500
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
