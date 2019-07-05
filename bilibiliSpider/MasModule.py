'''
Masquerading Module
'''
import random
import time

def mas_random_stop(begin=0, end=0.1):
    sleep_time = random.uniform(begin, end)
    time.sleep(sleep_time)


