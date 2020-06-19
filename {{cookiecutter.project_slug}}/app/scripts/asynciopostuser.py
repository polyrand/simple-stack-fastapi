import asyncio
import sys
from aiohttp import request
from aiomultiprocess import Pool
from itertools import repeat
from app.testutils import random_string, mail_generator
import time
import os

URL = os.getenv("URL", "http://localhost/api/v1/users/")


async def post(params):
    async with request(
        "POST", URL, json=params
    ) as response:
        # print(dir(response))
        if response.status != 200:
            print(response.status)
            print(response)
        # print(response.status)


def build_datapoints(n):
    assert n
    data = []
    for _ in range(n):
        new_datapoint = {
            "first_name": random_string(14),
            "last_name": random_string(14),
            "email": mail_generator(3, 45),
            "city": random_string(20),
        }
        data.append(new_datapoint)

    return data


async def main(data):
    async with Pool() as pool:
        result = await pool.map(post, data)


if __name__ == "__main__":
    print(URL)
    data = build_datapoints(n=int(sys.argv[1]))
    start = time.time()
    asyncio.run(main(data))
    end = time.time()
    print(f"done in {end-start}")
