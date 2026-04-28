from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    username = data.get('username')
    stars = data.get('stars')
    
    if not username or not stars:
        return jsonify({"error": "Missing username or stars"}), 400
    
    # Запускаем скрипт покупки
    result = subprocess.run(
        ['python', 'buy_stars.py', f'--username={username}', f'--stars={stars}'],
        capture_output=True, text=True
    )
    
    output = json.loads(result.stdout)
    if output.get('success'):
        return jsonify({"status": "ok", "tx": output.get('tx_id')})
    else:
        return jsonify({"error": output.get('error')}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
