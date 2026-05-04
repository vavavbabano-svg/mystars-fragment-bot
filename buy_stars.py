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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    clean_username = username.replace('@', '')
    
    # Шаг 1: Получаем wallet address пользователя
    info_url = f'https://fragment.com/api?hash={clean_username}'
    resp = requests.get(info_url, headers=headers)
    
    if resp.status_code != 200:
        print(f"Error getting user info: {resp.status_code}")
        return False
    
    user_data = resp.json()
    wallet_address = user_data.get('wallet') or user_data.get('address')
    
    if not wallet_address:
        print(f"Cannot find wallet for {clean_username}")
        return False
    
    # Шаг 2: Покупаем звёзды
    buy_url = f'https://fragment.com/stars/buy?recipient={wallet_address}&quantity={stars}'
    resp = requests.post(buy_url, headers=headers)
    
    if resp.status_code == 200:
        result = resp.json()
        if result.get('ok') or result.get('success'):
            print(f"Stars purchased: {json.dumps(result)}")
            return True
        else:
            print(f"Fragment error: {json.dumps(result)}")
            return False
    else:
        print(f"HTTP Error: {resp.status_code}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--stars', type=int, required=True)
    args = parser.parse_args()
    
    success = buy_stars(args.username, args.stars)
    if not success:
        sys.exit(1)
