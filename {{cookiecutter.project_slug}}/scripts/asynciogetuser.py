import asyncio
import time
import sys
from aiohttp import request
from aiomultiprocess import Pool
from itertools import repeat
import os

URL = os.getenv("URL", "http://localhost/api/v1/users/")


async def get(url):
    #     if sys.argv[1] == 1:
    #         print("Only 1")
    #         start_single = time.time()
    async with request("GET", url) as response:
        #         try:
        response = await response.text("utf-8")
        return response


#         finally:
#             if sys.argv[1] == 1:
#                 end_single = time.time()
#                 print(f"single done in {end_single-start_single}")


async def main():
    urls = list(repeat(URL, int(sys.argv[1])))
    async with Pool() as pool:
        result = await pool.map(get, urls)


if __name__ == "__main__":
    print(URL)
    print(f"n --> {sys.argv[1]}")
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"done in {end-start}")
