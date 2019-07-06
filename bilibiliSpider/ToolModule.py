import time

logging_path = 'logging.txt'

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
    with open(logging_path, 'a+', encoding='utf-8', newline='') as file:
        file.write(line+'\n')

