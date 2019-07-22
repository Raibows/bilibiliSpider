import asyncio
import time
import aiohttp



async def co_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)
            return await response.text()


# async def co_fetch(url):
#     response = await co_request(url)
#     html = await response.text()
#     return html

async def main(url, num:int):
    url = [
        r'http://127.0.0.1:5000/',
        r'http://127.0.0.1:5000/',
        r'http://127.0.0.1:5000/',
    ]
    tasks = [co_request(url[_i]) for _i in range(num)]
    # tasks = asyncio.create_task(co_fetch(url[0]))
    # done, pending = await asyncio.wait({tasks})
    done = await asyncio.gather(*tasks)
    for r in done:
        print(r)


if __name__ == '__main__':
    url = r'http://127.0.0.1:5000/'

    asyncio.run(main(url, 3))
    # main(url, 3)
    print(123)
    # for item in ans:
    #     done, pending = item
    #     print(done)
    #     print(pending)