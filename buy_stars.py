#!/usr/bin/env python3
import os
import json
import asyncio
import argparse
from pyfragment import FragmentClient

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
    if not seed:
        print(json.dumps({"success": False, "error": "TON_SEED missing"}))
        return

    async with FragmentClient(seed=seed) as client:
        try:
            result = await client.purchase_stars(username, amount=stars)
            print(json.dumps({
                "success": True,
                "username": result.username,
                "stars": result.amount,
                "tx_id": result.transaction_id
            }))
        except Exception as e:
            print(json.dumps({"success": False, "error": str(e)}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--stars", type=int, required=True)
    args = parser.parse_args()
    asyncio.run(buy_stars(args.username, args.stars))
