_output_path = r'C:\Users\Raibows\PycharmProjects\bilibilivideohot\bilibili_rank_data.csv'
_logging_path = r'C:\Users\Raibows\PycharmProjects\bilibilivideohot\logging.txt'
_multi_processor_flag = False
_mas_proxy_flag = True
_ip_proxy_pool_addr = '127.0.0.1:5010'


# _output_path = r'/home/chizuo/projects/bilibilivideohot/bilibili_rank_data.csv'
# _logging_path = r'/home/chizuo/projects/bilibilivideohot/logging.txt'




class spider_config():
    current_path = None
    logging_path = _logging_path
    output_path = _output_path
    mas_proxy_flag = _mas_proxy_flag
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
    multi_processor_flag = _multi_processor_flag
    mas_proxy_pool_ip = _ip_proxy_pool_addr
