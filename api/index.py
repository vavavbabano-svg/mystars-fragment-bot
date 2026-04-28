import os
from flask import Flask, request, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))

@app.route('/buy', methods=['POST'])
def buy():
    # Просто логируем, что запрос пришёл
    print("Получен запрос!")

    # Всегда возвращаем успех, чтобы Lava не дублировала
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
