import requests
import time
import asyncio


async def fetcher():
    print('request called')
    url = "http://localhost:8000/user"

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print('called')
    # print(response.text)


async def main():
    await asyncio.gather(
        fetcher(),
        fetcher(),
        fetcher(),
        fetcher(),
        fetcher(),
    )


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end-start)