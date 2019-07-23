from redis import StrictRedis
import ProxyPool
import json


class redis_db():
    '''
    Further Encapsulate Redis
    '''
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.__redis = StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    def get_proxy(self):
        pass
    def delete_all(self):
        self.__redis.flushdb()
    def add_proxy(self, proxies):
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
        return self.__redis.randomkey()

    def get_one_dict(self):
        '''
        :return:dictionary, proxy
        '''
        dict_proxy = self.__redis.get(self.__redis.randomkey())
        dict_proxy = json.loads(dict_proxy)
        return dict_proxy



if __name__ == '__main__':

    # test = redis_db()
    # test.delete_all()
    # a = ProxyPool.proxy('192.141.32.2', '2367')
    # b = ProxyPool.proxy('111.23.214.123', '23')
    # test.add_proxy([a, b])
    # print(type(test.get_one_dict()))

    pass
