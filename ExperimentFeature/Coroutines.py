import asyncio
import time
import aiohttp



async def co_request(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        # print(response)
        return response


async def co_fetch(url):
    response = await co_request(url)
    html = await response.text()
    return html

async def main(url, num:int):
    tasks = [asyncio.create_task(co_fetch(url)) for _ in range(num)]
    await asyncio.gather(asyncio.wait(tasks))
    for _i in range(num):
        print(tasks[_i].result())


if __name__ == '__main__':
    url = r'http://127.0.0.1:5000/'

    asyncio.run(main(url, 3))

    print(123)
    # for item in ans:
    #     done, pending = item
    #     print(done)
    #     print(pending)