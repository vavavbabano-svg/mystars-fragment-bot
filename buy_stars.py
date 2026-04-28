import os
import sys
import asyncio
import argparse
from pyfragment import FragmentClient

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
    if not seed:
        raise Exception("TON_SEED not configured")
    
    async with FragmentClient(seed=seed) as client:
        result = await client.purchase_stars(username, amount=stars)
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--stars", type=int, required=True)
    args = parser.parse_args()
    
    asyncio.run(buy_stars(args.username, args.stars))
