import os
import sys
import asyncio
import argparse
from fragment_api_lib.client import FragmentAPIClient

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
    fragment_cookies = os.environ.get("FRAGMENT_COOKIES", "")
    
    if not seed:
        print("ERROR: TON_SEED not configured")
        sys.exit(1)
    
    client = FragmentAPIClient()
    
    # Основной метод покупки (с поддержкой KYC)
    result = client.buy_stars(
        username=username,
        amount=stars,
        show_sender=False,
        fragment_cookies=fragment_cookies,
        seed=seed
    )
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--stars", type=int, required=True)
    args = parser.parse_args()
    
    result = asyncio.run(buy_stars(args.username, args.stars))
    print(f"Purchase result: {result}")
