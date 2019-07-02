import threading
import time
from queue import Queue

def thread_job():
    print('this is an added threading, num is {}'.format(threading.current_thread()))
    time.sleep(10)
def main():
    added_thread = threading.Thread(target=thread_job)
    added_thread.start()
    added_thread.join() #it will not excute next line
                        #until the joined thread has done



def job(l, q):
    for i in range(len(l)):
        print('this is {} and i is {}'.format(threading.current_thread(), i))
        time.sleep(3)
        l[i] = l[i] ** 2
    q.put(l)

def multiThreading(data):
    q = Queue()
    threads = []
    for i in range(4):
        t = threading.Thread(target=job, args=(data[i], q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
        print('gggggg')

    results = []
    for _ in range(4):
        results.append(q.get())
    print(results)

if __name__ == '__main__':
    print(threading.active_count())
    # data = [[1,2,3], [4,5,5], [2,1,2], [3,3,0]]
    # multiThreading(data)
    
