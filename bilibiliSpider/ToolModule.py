import time
from bilibiliSpider import Config

default_logging_path = Config.spider_config.logging_path
def tool_get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return current_time

def tool_log_info(level='info', message='NOTHING'):
    '''
    :param level: info or error
    :param message:
    :return:
    '''
    line = level + '  ' + message + '  ' + tool_get_current_time()
    with open(default_logging_path, 'a+', encoding='utf-8', newline='') as file:
        file.write(line+'\n')

def tool_count_time(func):
    def wrapper(*args, **kwargs):
        time1 = time.clock()
        func(*args, **kwargs)
        print(func.__name__, 'costs', time.clock() - time1, 'seconds')
    return wrapper