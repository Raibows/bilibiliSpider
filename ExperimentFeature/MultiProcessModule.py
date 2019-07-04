from bilibiliSpider import SpiderModule
import multiprocessing as mp
import time
import threading
import queue as q




def count_time(func):
    def wrapper(*args, **kwargs):
        time1 = time.clock()
        func(*args, **kwargs)
        print(func.__name__, time.clock() - time1)
    return wrapper


def job(rank_type, video_type, lock=None):
    test = SpiderModule.bilibili_spider()
    x = test.get_rank_video_info(rank_type=rank_type, video_type=video_type)
    print(video_type)
    return x



@count_time
def multi_process(category = ('all', 'movie')):
    res = []
    pool = mp.Pool(processes=3)
    for i in category:
        x = pool.apply_async(job, args=('origin', i))
        res.append(x)
    pool.close()
    pool.join()
    for i in res:
        print(i.get())




if __name__ == '__main__':
    category = ('all', 'movie', 'game', 'dance')
    res = multi_process(category=category)
