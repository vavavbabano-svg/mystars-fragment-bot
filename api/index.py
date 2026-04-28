import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))

@app.route('/buy', methods=['POST'])
def buy():
    try:
        # Логируем входящий запрос (для отладки)
        print("Headers:", dict(request.headers))
        print("Raw data:", request.get_data(as_text=True))
        
        # Парсим JSON от Lava
        data = request.get_json()
        print("Parsed JSON:", data)
        
        # Пробуем вытащить username и stars в любом возможном месте
        username = None
        stars = None
        
        # Способ 1: прямые поля
        if 'username' in data:
            username = data['username']
            stars = data.get('stars')
        # Способ 2: вложенные в custom_fields
        elif 'custom_fields' in data and data['custom_fields']:
            custom = json.loads(data['custom_fields']) if isinstance(data['custom_fields'], str) else data['custom_fields']
            username = custom.get('username')
            stars = custom.get('stars')
        # Способ 3: в объекте data (если вся структура другая)
        elif 'data' in data:
            username = data['data'].get('username')
            stars = data['data'].get('stars')
        
        if not username or not stars:
            return jsonify({"error": "Missing username or stars", "received": data}), 400
        
        # Здесь будет покупка звёзд (пока заглушка)
        # TODO: запустить buy_stars.py
        
        return jsonify({"status": "ok", "username": username, "stars": stars}), 200
        
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
