import os
import asyncio
import argparse
from fragment_api_lib.client import FragmentAPIClient
from fragment_api_lib.models import *

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
    fragment_cookies = os.environ.get("FRAGMENT_COOKIES", "")
    
    if not seed:
        raise Exception("TON_SEED not configured")
    
    client = FragmentAPIClient()
    
    # Покупка звёзд (с KYC, через cookies)
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
    
    asyncio.run(buy_stars(args.username, args.stars))
