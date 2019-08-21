'''
Configuration file
'''


def print_all_config_info():
    print(spider_config())
    print(toolbox_config())
    print(proxypool_config())
    print(flaskserver_config())


def get_all_config_json():
    '''
    return all the config classes in Config.py with json
    :return:
    '''
    import json
    info = []
    config_json = {}

    info.append(spider_config().get_config_dict())
    info.append(toolbox_config().get_config_dict())
    info.append(proxypool_config().get_config_dict())
    info.append(flaskserver_config().get_config_dict())

    for config in info:
        config_json[config[0]] = config[1]

    config_json = json.dumps(config_json)

    return config_json



class repr_base_class:
    def __repr__(self):
        base_place =  '-'
        head = type(self).__name__
        info = head + 40 * base_place + '\n'
        # print(dir(self))
        for attr in dir(self):
            if not callable(attr) and not attr.startswith("__") and attr != 'get_config_dict':
                temp = f'{attr}: {self.__getattribute__(attr)}'
                base_place_pos = len(head) + 40 - len(temp) - 1
                temp = temp + base_place_pos * ' ' + '|'
                info = info + temp + '\n'

        info += (len(head) + 40) * base_place
        info += '\n'
        return info

    def get_config_dict(self):
        '''
        :return:class name, config_json(dict)
        '''
        config_dict = {}
        for attr in dir(self):
            if not callable(attr) and not attr.startswith("__") and attr != 'get_config_dict':
                config_dict[attr] = self.__getattribute__(attr)
        print(config_dict)
        return type(self).__name__, config_dict






class spider_config(repr_base_class):
    current_path = None
    output_path = r'../data/bilibili_rank_data.csv'
    mas_proxy_flag = False
    tasks = [
        'all',
        'animation',
        'guochuang',
        'music',
        'dance',
        'game',
        'technology',
        'digital',
        'life',
        'guichu',
        'fashion',
        'entertainment',
        'movie'
    ]
    rank_type = 'origin' #or all
    multi_processor_flag = True
    mas_proxy_pool_ip = '127.0.0.1:5010'
    multi_processor_num = 2
    coroutine = True # can't change



class toolbox_config(repr_base_class):
    logging_path = r'../data/logging.txt'
    fake_header_browser = 'Chrome'


class proxypool_config(repr_base_class):
    check_interval = 150 #seconds
    spider_interval = 300 #seconds
    print_interval = 15
    evaluate_interval = 30
    check_proxy_timeout = 10
    coroutines_semaphore = 10 #limit the number of coroutines

    database_type = 'Redis'
    database_host = 'localhost'
    database_port = '6379'
    database_password = None
    database_init_flushall = True


class flaskserver_config(repr_base_class):
    flaskserver_host = '127.0.0.1'
    flaskserver_port = 5010
    flaskserver_threaded = True
    flask_base_api = f'http://{flaskserver_host}:{flaskserver_port}/proxy/'
    flask_get_one_api = {
        'string': flask_base_api + 'get_one/string',
        'dict': flask_base_api + 'get_one/dict',
    }
    flask_all_config_api = flask_base_api + 'config'
    flask_feedback_api = flask_base_api + 'feedback'




if __name__ == '__main__':
    print_all_config_info()
    # print(spider_config())
    # temp = get_all_config_json()
    # import json
    # print(json.loads(temp))