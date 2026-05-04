import os
import json
import requests
import argparse
import time

FRAGMENT_COOKIE = os.environ.get('FRAGMENT_COOKIE', '')

def buy_stars(username, stars):
    if not FRAGMENT_COOKIE:
        print("ERROR: FRAGMENT_COOKIE not set")
        return False
    
    headers = {
        'Cookie': FRAGMENT_COOKIE,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    clean_username = username.replace('@', '')
    
    # Шаг 1: Получаем информацию о пользователе
    url = f'https://fragment.com/api?hash={clean_username}'
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        print(f"Error getting user info: {resp.status_code}")
        return False
    
    # Шаг 2: Покупаем звёзды
    buy_url = 'https://fragment.com/api/buyStars'
    data = {
        'username': clean_username,
        'amount': stars
    }
    
    resp = requests.post(buy_url, json=data, headers=headers)
    
    if resp.status_code == 200:
        result = resp.json()
        print(f"Stars purchased: {json.dumps(result)}")
        return True
    else:
        print(f"Error buying stars: {resp.status_code} {resp.text}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--stars', type=int, required=True)
    args = parser.parse_args()
    
    success = buy_stars(args.username, args.stars)
    if not success:
        sys.exit(1)
