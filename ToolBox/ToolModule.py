import time
import random
from Config import toolbox_config
from fake_headers import Headers




default_fake_header_browser = toolbox_config.fake_header_browser
default_logging_path = toolbox_config.logging_path


headers = Headers(browser=default_fake_header_browser)

def tool_get_current_time():
    '''
    :return: string, get current time like 2019-12-08 12:32:28
    '''
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return current_time

def tool_log_info(level='info', message='NOTHING'):
    '''
    :param level: info or error
    :param message:
    :return:store the logging info
    '''
    line = level + '  ' + message + '  ' + tool_get_current_time()
    with open(default_logging_path, 'a+', encoding='utf-8', newline='') as file:
        file.write(line+'\n')

def tool_count_time(func):
    '''
    a decorator that static the cost time
    :param func:
    :return:
    '''
    def wrapper(*args, **kwargs):
        time1 = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__, 'costs', time.clock() - time1, 'seconds')
        return res
    return wrapper

def tool_stop_random_time(min_time=0, max_time=1):
    '''
    sleep random [min_time, max_time) time
    :param min_time:
    :param max_time:
    :return:
    '''
    random_time = random.uniform(min_time, max_time)
    time.sleep(random_time)

def tool_get_random_headers():
    '''
    :return: fake headers
    '''
    return headers.generate()


if __name__ == '__main__':
    tool_stop_random_time()