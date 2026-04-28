import os
import sys
import asyncio
import argparse
from pyfragment import FragmentClient

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
    api_key = os.environ.get("TONAPI_KEY", "")  # берём ключ из переменных окружения
    cookies_str = os.environ.get("FRAGMENT_COOKIES", "")
    
    if not seed:
        raise Exception("TON_SEED not configured")
    
    # Парсим cookies в словарь (если есть)
    cookies = {}
    if cookies_str:
        for item in cookies_str.split('; '):
            if '=' in item:
                key, value = item.split('=', 1)
                cookies[key] = value
    
    # Передаём api_key в FragmentClient
    async with FragmentClient(seed=seed, api_key=api_key, cookies=cookies) as client:
        result = await client.purchase_stars(username, amount=stars)
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--stars", type=int, required=True)
    args = parser.parse_args()
    
    asyncio.run(buy_stars(args.username, args.stars))
