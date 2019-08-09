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
        size = self.__redis.dbsize()
        if size:
            return self.__redis.dbsize()
        else:
            return 0

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
        # print(f'Redis num {self.get_num()}')

    def get_one_string(self) ->str or None:
        '''
        :return:string, proxy
        '''
        if self.get_num():
            byte_ = self.__redis.randomkey()
            str_ = str(byte_, encoding='utf-8')
            return str_
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
        # print(f'Redis num {self.get_num()}')

    def proxy_feedback(self, proxy_string_dict, flag:bool):
        '''
        through this func to adjust proxy points
        when you get a proxy from database
        if flag == False, then the proxy's points will be decreased
        == True, then the proxy's points will be increased
        :return: insert a special message to the database
        '''
        res = proxy_string_dict
        if type(proxy_string_dict) == dict:
            res = proxy_string_dict['http']
        if flag:
            self.__redis.rpush('increase', res)
        else:
            self.__redis.rpush('decrease', res)

    def get_feedback(self) -> dict:
        feedback = {}
        info = []
        temp = self.__redis.rpop('increase')
        while temp:
            temp = bytes.decode(temp)
            info.append(temp)
            temp = self.__redis.rpop('increase')
        feedback['increase'] = info
        info = []
        temp = self.__redis.rpop('decrease')
        while temp:
            temp = bytes.decode(temp)
            info.append(temp)
            temp = self.__redis.rpop('decrease')
        feedback['decrease'] = info

        return feedback




if __name__ == '__main__':

    test = database()
    proxy = 'http://119.254.94.114:34422'
    # test.proxy_feedback(proxy, True)
    #
    a = ProxyPool.proxy('192.141.32.2', '2367')
    b = ProxyPool.proxy('111.23.214.123', '23')
    c = ProxyPool.proxy('111.23.214.123', '231')
    test.add_proxies([a, b, c])


    # test.delete_proxies([a, b])
    # test.add_proxies([a, b, c])
    # test.add_proxies([a, b, c])
    #
    # test.proxy_feedback(a.get_string_address(), True)
    # test.proxy_feedback(a.get_dict_address(), False)
    # test.proxy_feedback(b.get_dict_address(), True)
    #
    # print(test.get_feedback())

    # temp = test.get_all_increase()
    # print(type(temp[0]))
    # test.proxy_feedback(a.get_dict_address())
    # print(a.get_string_address())
    # # print(type(test.get_one_dict()))
    #
    # import requests
    # url = 'http://127.0.0.1:5010/proxy/get_one/dict'
    # x = requests.get(url)
    # x = json.loads(x.text)
    # print('zzz', type(x))

    pass
