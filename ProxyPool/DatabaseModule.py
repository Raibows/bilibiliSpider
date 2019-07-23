from redis import StrictRedis
import json
import ToolBox
from Config import proxypool_config
import ProxyPool



default_database_type = proxypool_config.database_type
default_database_host = proxypool_config.database_host
default_database_port = proxypool_config.database_port
default_database_password = proxypool_config.database_password
default_database_flushall = proxypool_config.database_init_flushall



class database():
    '''
    Further Encapsulate Redis
    '''
    def __init__(self, host=default_database_host, port=default_database_port, db=0, password=default_database_password):
        if default_database_type.lower() == 'redis':
            self.__redis = StrictRedis(
                host=host,
                port=port,
                db=db,
                password=password
            )
            if default_database_flushall:
                self.delete_all() #WARNING
        else:
            raise ToolBox.ConfigError('Only support Redis database now !')

    def get_num(self):
        '''
        :return:int, num of keys in database
        '''
        return self.__redis.dbsize()

    def delete_all(self):
        self.__redis.flushdb()
        print(f'Redis has been flushed all {ToolBox.tool_get_current_time()}')

    def add_proxies(self, proxies):
        if proxies:
            data = {}
            for proxy in proxies:
                string_proxy = proxy.get_string_address()
                dict_proxy = json.dumps(proxy.get_dict_address())
                data[string_proxy] = dict_proxy
            self.__redis.mset(data)

    def get_one_string(self):
        '''
        :return:string, proxy
        '''
        if self.get_num():
            return self.__redis.randomkey()
        else:
            return None

    def get_one_dict(self):
        '''
        :return:dictionary, proxy
        '''
        if self.get_num():
            dict_proxy = self.__redis.get(self.__redis.randomkey())
            dict_proxy = json.loads(dict_proxy)
            return dict_proxy
        else:
            return None

    def delete_proxies(self, proxies):
        '''
        delete the proxies from database
        :param proxies: proxy object list
        :return: None
        '''
        if proxies:
            for proxy in proxies:
                self.__redis.delete(proxy.get_string_address())


if __name__ == '__main__':

    test = database()
    #
    a = ProxyPool.proxy('192.141.32.2', '2367')
    b = ProxyPool.proxy('111.23.214.123', '23')
    c = ProxyPool.proxy('111.23.214.123', '231')
    # test.delete_proxies([a, b])
    # test.add_proxies([a, b, c])
    # test.add_proxies([a, b, c])
    test.delete_proxies([a])

    print(test.get_one_dict())
    # print(type(test.get_one_dict()))

    pass
