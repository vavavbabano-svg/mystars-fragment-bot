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
        'User-Agent': 'Mozilla/5.0'
    }
    
    clean_username = username.replace('@', '')
    
    # Покупаем звёзды
    buy_url = f'https://fragment.com/stars/buy?recipient={clean_username}&quantity={stars}'
    resp = requests.post(buy_url, headers=headers)
    
    if resp.status_code == 200:
        print(f"Stars purchased for {clean_username}")
        return True
    else:
        print(f"Error: {resp.status_code} {resp.text}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--stars', type=int, required=True)
    args = parser.parse_args()
    
    success = buy_stars(args.username, args.stars)
    if not success:
        sys.exit(1)
