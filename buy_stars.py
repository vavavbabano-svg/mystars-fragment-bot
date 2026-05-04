import os
import sys
import json
import asyncio
import argparse
import httpx

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
    fragment_cookies = os.environ.get("FRAGMENT_COOKIE", "")
    
    if not seed:
        print("ERROR: TON_SEED not configured")
        sys.exit(1)
    
    clean_username = username.replace('@', '')
    
    headers = {
        "Cookie": fragment_cookies,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        info_url = f"https://fragment.com/api?hash={clean_username}"
        resp = await client.get(info_url, headers=headers)
        print(f"Info: {resp.status_code}")
        
        buy_url = "https://fragment.com/api/buyStars"
        payload = {
            "username": clean_username,
            "amount": stars
        }
        resp = await client.post(buy_url, json=payload, headers=headers)
        print(f"Buy: {resp.status_code} {resp.text}")
        
        if resp.status_code == 200:
            return True
        else:
            print(f"Error: {resp.text}")
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--stars", type=int, required=True)
    args = parser.parse_args()
    
    result = asyncio.run(buy_stars(args.username, args.stars))
    if not result:
        sys.exit(1)
