import os
import asyncio
import argparse
from pyfragment import FragmentClient

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
    cookies_str = os.environ.get("FRAGMENT_COOKIES")
    cookies = dict(x.split('=', 1) for x in cookies_str.split('; ') if x) if cookies_str else None
    
    async with FragmentClient(seed=seed, cookies=cookies) as client:
        result = await client.purchase_stars(username, amount=stars)
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--stars", type=int, required=True)
    args = parser.parse_args()
    
    asyncio.run(buy_stars(args.username, args.stars))
    cookies_str = os.environ.get("FRAGMENT_COOKIES")
print(f"Cookies loaded: {cookies_str[:50]}...")  # покажет первые 50 символов
