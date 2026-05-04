import os
import sys
import asyncio
import argparse
import http.cookies
from fragment_api_lib.client import FragmentAPIClient

async def buy_stars(username: str, stars: int):
    seed = os.environ.get("TON_SEED")
fragment_cookies = os.environ.get("FRAGMENT_COOKIE", "")
    
    if not seed:
        print("ERROR: TON_SEED not configured")
        sys.exit(1)
    
    # Преобразуем куки в Header String если они ещё не в том формате
    if not fragment_cookies.startswith("Cookie:"):
        # Убираем лишние пробелы и переносы
        fragment_cookies = fragment_cookies.strip().replace('\n', '')
        # Форматируем как Header String
        fragment_cookies = f"Cookie: {fragment_cookies}"
    
    client = FragmentAPIClient()
    
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
