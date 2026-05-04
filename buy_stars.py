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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    clean_username = username.replace('@', '')
    
    # Покупаем звёзды через Fragment API
    buy_url = f'https://fragment.com/api?hash={clean_username}'
    data = {
        'type': 'stars',
        'amount': stars
    }
    
    resp = requests.post(buy_url, json=data, headers=headers)
    
    if resp.status_code == 200:
        result = resp.json()
        if result.get('ok') or result.get('success'):
            print(f"Stars purchased: {json.dumps(result)}")
            return True
        else:
            print(f"Fragment error: {json.dumps(result)}")
            return False
    else:
        print(f"HTTP Error: {resp.status_code} {resp.text}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--stars', type=int, required=True)
    args = parser.parse_args()
    
    success = buy_stars(args.username, args.stars)
    if not success:
        sys.exit(1)
