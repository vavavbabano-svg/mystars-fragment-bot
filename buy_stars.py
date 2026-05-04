import os
import sys
import json
import requests
import argparse

FRAGMENT_COOKIE = os.environ.get('FRAGMENT_COOKIE', '')

def buy_stars(username, stars):
    if not FRAGMENT_COOKIE:
        print("ERROR: FRAGMENT_COOKIE not set")
        return False
    
    headers = {
        'Cookie': FRAGMENT_COOKIE,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Origin': 'https://fragment.com',
        'Referer': 'https://fragment.com/'
    }
    
    clean_username = username.replace('@', '')
    
    # Сначала получаем токен
    token_url = 'https://fragment.com/api?hash=' + clean_username
    resp = requests.get(token_url, headers=headers)
    print(f"Token response: {resp.status_code} {resp.text[:200]}")
    
    if resp.status_code != 200:
        print(f"Error getting token: {resp.status_code}")
        return False
    
    # Покупаем звёзды
    buy_url = f'https://fragment.com/stars/buy?recipient={clean_username}&quantity={stars}'
    resp = requests.post(buy_url, headers=headers)
    print(f"Buy response: {resp.status_code} {resp.text[:200]}")
    
    # Проверяем результат
    if 'success' in resp.text.lower() or 'ok' in resp.text.lower():
        print(f"Stars purchased for {clean_username}")
        return True
    elif resp.status_code == 200:
        print(f"Stars likely purchased (status 200): {resp.text[:100]}")
        return True
    else:
        print(f"Error buying stars: {resp.status_code}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--stars', type=int, required=True)
    args = parser.parse_args()
    
    success = buy_stars(args.username, args.stars)
    if not success:
        sys.exit(1)
