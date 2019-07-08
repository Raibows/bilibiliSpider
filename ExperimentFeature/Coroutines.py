import asyncio
import time
import os
import subprocess


async def say_word(time, word):
    await asyncio.sleep(time)
    print(word)

async def main():

    task1 = asyncio.create_task(
        say_word(1, 'hello')
    )
    task2 = asyncio.create_task(
        say_word(2, 'world')
    )
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


async def get_time():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5
    while True:
        print(f"now time is {time.strftime('%X')}")
        if (loop.time() + 1) > end_time:
            break
        await asyncio.sleep(1)

# asyncio.run(get_time())

