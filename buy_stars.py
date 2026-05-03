import os
import json
import re
import subprocess
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))

VPN_BOT_TOKEN = '8776699039:AAEwnKj7juy4mmZWtSrKoJKVFovyX8D4y1Q'

def send_vpn_key(chat_id):
    """Отправляет запрос на создание VPN-ключа и возвращает ссылку"""
    try:
        res = requests.post('http://194.87.134.111:3000/create-key', timeout=10)
        data = res.json()
        if data.get('success') and data.get('link'):
            # Отправляем ключ пользователю через бота
            requests.post(
                f'https://api.telegram.org/bot{VPN_BOT_TOKEN}/sendMessage',
                json={
                    'chat_id': chat_id,
                    'text': '🔒 *Ваш VPN-ключ:*\n\n`' + data['link'] + '`\n\nСкопируйте и вставьте в HAPP VPN.',
                    'parse_mode': 'Markdown'
                }
            )
            print(f"VPN key sent to {chat_id}")
    except Exception as e:
        print(f"VPN error: {e}")

@app.route('/buy', methods=['POST'])
def buy():
    try:
        print("Headers:", dict(request.headers))
        print("Raw data:", request.get_data(as_text=True))
        
        data = request.get_json()
        print("Parsed JSON:", data)
        
        username = None
        stars = None
        
        if 'username' in data:
            username = data['username']
            stars = data.get('stars')
        elif 'custom_fields' in data and data['custom_fields']:
            custom = json.loads(data['custom_fields']) if isinstance(data['custom_fields'], str) else data['custom_fields']
            username = custom.get('username')
            stars = custom.get('stars')
        elif 'data' in data:
            username = data['data'].get('username')
            stars = data['data'].get('stars')
        
        if not username or not stars:
            order_id = data.get('order_id', '')
            match = re.search(r'([a-zA-Z0-9_]+)_stars_(\d+)', order_id)
            if match:
                username = '@' + match.group(1)
                stars = int(match.group(2))
                print(f"Extracted from order_id: username={username}, stars={stars}")
        
        if not username or not stars:
            print("ERROR: Missing username or stars")
            return jsonify({"error": "Missing username or stars", "received": data}), 400
        
        print(f"OK: username={username}, stars={stars}")
        
        # Покупаем звёзды
        result = subprocess.run(
            ['python', 'buy_stars.py', '--username', username, '--stars', str(stars)],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"Stars purchased: {result.stdout}")
            
            # Дополнительно: если это VPN платёж — отправляем ключ
            if 'VPN' in str(data.get('description', '')) or 'vpn' in str(data.get('order_id', '')).lower():
                # Получаем chat_id из custom_fields
                chat_id = None
                try:
                    custom = json.loads(data.get('custom_fields', '{}')) if isinstance(data.get('custom_fields'), str) else data.get('custom_fields', {})
                    chat_id = custom.get('chat_id')
                except:
                    pass
                
                if chat_id:
                    send_vpn_key(chat_id)
            
            return jsonify({"status": "ok", "message": f"Stars sent to {username}"}), 200
        else:
            print(f"Error: {result.stderr}")
            return jsonify({"error": result.stderr}), 500
        
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
