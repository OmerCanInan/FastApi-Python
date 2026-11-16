import asyncio
import time

import httpx

URL = "https://httpbin.org/delay/2"


def senkron() -> None:
    for i in range(5):
        r = httpx.get(URL, timeout=15)
        print(f"Senkron {i + 1}: {r.status_code}")


async def tek_istek(client: httpx.AsyncClient, sem: asyncio.Semaphore, no: int) -> None:
    async with sem:
        print(f"  {no} başladı")
        r = await client.get(URL)
        print(f"  {no} bitti: {r.status_code}")


async def ana(limit: int) -> None:
    sem = asyncio.Semaphore(limit)
    async with httpx.AsyncClient(timeout=30) as client:
        isler = [tek_istek(client, sem, i + 1) for i in range(5)]
        await asyncio.gather(*isler)


for limit in (1, 3, 5):
    print(f"Semaphore({limit})")
    t = time.perf_counter()
    asyncio.run(ana(limit))
    print(f"Süre: {time.perf_counter() - t:.2f} sn\n")