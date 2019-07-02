import multiprocessing as mp
import threading as td
import time, queue


def count_time(func):
    def wrapper(args, *kwargs):
        time1 = time.clock()
        func(args, *kwargs)
        print(func.__name__, time.clock() - time1)
    return wrapper


def job(q, a):
    res = 0
    for i in range(a):
        res += i ** 3.491
    q.put(res)
    # print(mp.current_process())

@count_time
def multi_process(num):
    queue = mp.Queue()
    p1 = mp.Process(target=job, args=(queue, num))
    p2 = mp.Process(target=job, args=(queue, num))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    # print(queue.get())
    # print(queue.get())


@count_time
def multi_thread(num):
    q = queue.Queue()
    t1 = td.Thread(target=job, args=(q, num))
    t2 = td.Thread(target=job, args=(q, num))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # print(q.get())
    # print(q.get())

@count_time
def single(num):
    q = queue.Queue()
    job(q, num)
    job(q, num)
    # print(q.get())
    # print(q.get())

@count_time
def list_test(num):
    x = [i ** 3.491 for i in range(num)]
    x = [i ** 3.491 for i in range(num)]

if __name__ == '__main__':
    num = 10000000
    multi_process(num)
    time.sleep(5)
    multi_thread(num)
    time.sleep(5)
    single(num)
    time.sleep(5)
    list_test(num)

