




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
    multi_processor_num = 2
    def __repr__(self):
        return f"""
        current_path: {self.current_path}
        logging_path: {self.logging_path}
        output_path: {self.output_path}
        tasks: {self.tasks}
        mas_proxy_flag: {self.mas_proxy_flag}
        mas_proxy_pool_ip: {self.mas_proxy_pool_ip}
        multi_processor_flag: {self.multi_processor_flag}
        multi_processor_num: {self.multi_processor_num}
        """
