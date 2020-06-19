import asyncio
import sys
from aiohttp import request
from aiomultiprocess import Pool
from itertools import repeat
from app.testutils import random_string, mail_generator
import time
import os

URL = os.getenv("URL", "http://localhost/api/v1/items/")


async def post(params):
    async with request("POST", URL, json=params) as response:
        # print(dir(response))
        if response.status != 200:
            print("Status: ", response.status)
            print("Text: ", response.text)
            print("Response:", response)
        # print(response.status)


def build_datapoints(n):
    assert n
    data = []
    for _ in range(n):

        new_datapoint = {
            "title": random_string(15),
            "description": random_string(125),
            "city": random_string(15),
            "maps_url": "https://www.google.es/maps/place/Barcelona/@41.3947688,2.078728,12z/",
            "first_name": random_string(15),
            "last_name": random_string(15),
            "owner_email": mail_generator(3, 45),
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
