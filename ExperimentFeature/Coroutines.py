import asyncio
import time
import os
import subprocess
import csv
from bilibiliSpider import SpiderModule
from bilibiliSpider import ProcessRawModule
from bilibiliSpider import MasModule
from bilibiliSpider import ToolModule
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Queue













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


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial{i}")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial{number} = {f}")
    return f


async def main1():
    print(f"started at {time.strftime('%X')}")
    res = await asyncio.gather(
            factorial('a', 2),
            factorial('b', 3),
            factorial('c', 4),
        )
    print(f"finished at {time.strftime('%X')}")
    print(res)



default_spider = SpiderModule.bilibili_spider()
default_spider.mas_proxy_flag = False


def export_to_csv1(video_category, spider=default_spider, csv_path='bilibili_rank_data.csv', rank_type='origin'):
    # video_category = list(spider.video_category.keys())
    # video_category.remove('all')
    # video_category = ['all']
    # video_category = ['guochuang']
    video_category = [video_category]
    info = []
    head = ['0rank_type', '1video_type', '2video_id', '3ranking',
                 '4video_title', '5video_upload_time', '6video_length_time',
                 '7author_id', '8author_followers', '9author_following',
                 '10view', '11danmaku', '12reply', '13favorite', '14coin', '15share', '16like',
                 '17points', '18spider_time'
            ]
    info.append(head)
    count = 0
    for video_type in video_category:
        MasModule.mas_random_stop()
        videos = spider.get_rank_video_info(rank_type=rank_type, video_type=video_type)[1:]
        log = 'getting {} {}'.format(rank_type, video_type)
        print(log)
        info.append(videos)
        csv_path = f'test{video_type}.csv'
        for video in videos:
            with open('test.csv', 'a+', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(video)
    return info








def single_run(tasks):
    print(f"started at {time.strftime('%X')}")
    for task in tasks:
        res = export_to_csv1(task)
    print(f"finished at {time.strftime('%X')}")



def multi_run(tasks):
    print(f"started at {time.strftime('%X')}")
    MAX_WORKER_NUM = multiprocessing.cpu_count()
    p = Pool(MAX_WORKER_NUM)
    for task in tasks:
        print(task)
        p.apply_async(export_to_csv1, args=task)

    p.close()
    p.join()
    print(f"finished at {time.strftime('%X')}")

























if __name__ == '__main__':


    tasks = [['all'], ['movie'], ['guochuang'], ['music'], ['dance'], ['game'], ['life'], ['digital']]
    # asyncio.run(get_time())
    # asyncio.run(main1())
    multi_run(tasks=tasks)


    # time.sleep(10)

    # single_run(tasks=tasks)

