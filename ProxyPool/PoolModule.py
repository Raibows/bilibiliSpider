from Config import proxypool_config
import ProxyPool
from bs4 import BeautifulSoup
import threading
import aiohttp
import asyncio
import ToolBox



default_check_interval = proxypool_config.check_interval
default_spider_interval = proxypool_config.spider_interval
default_print_interval = proxypool_config.print_interval
default_check_proxy_timeout = proxypool_config.check_proxy_timeout


class proxy_pool():
    '''
    proxy pool
    use coroutines for spider on free-proxy web
    '''
    def __init__(self):
        self.__proxy_urls = [
            r'https://www.kuaidaili.com/free/inha/{}/'
        ]
        self.__test_ip_url = 'http://httpbin.org/ip'
        self.__pool = []
        self.__html_lib = None

        self.__check_interval = default_check_interval
        self.__spider_interval = default_spider_interval
        self.__print_interval = default_print_interval

        self.__db = ProxyPool.DatabaseModule.database()


    async def __get_html(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()


    def __evaluate_pool(self):
        delete_proxies = []
        for proxy in self.__pool:
            if proxy.points < 0:
                self.__pool.remove(proxy)
                delete_proxies.append(proxy)
                print(f'Delete {proxy}')
        self.__db.delete_proxies(delete_proxies)
        self.__db.add_proxies(self.__pool)


    async def __process_first_html(self):
        tasks = [self.__get_html(self.__proxy_urls[0].format(_i)) for _i in range(1, 2)]
        # print(tasks)
        # os._exit(-1)
        done = await asyncio.gather(*tasks)
        for html in done:
            # print(html)
            # os._exit(-1)
            soup = BeautifulSoup(html, features="html5lib")
            ips = soup.find_all(
                'td',
                {
                    'data-title': 'IP'
                }
            )
            ports = soup.find_all(
                'td',
                {
                    'data-title': 'PORT'
                }
            )
            proxies = zip(ips, ports)
            for item in proxies:
                proxy = ProxyPool.proxy(item[0].string, item[1].string)
                if item not in self.__pool:
                    self.__pool.append(proxy)
                    print(f'got {proxy.get_string_address()}')

    async def __check_available(self, proxy):
        proxy = proxy.get_string_address()
        print(f'checking {proxy}')
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(
                    url=self.__test_ip_url,
                    proxy=proxy,
                    timeout=default_check_proxy_timeout,
                    headers=ToolBox.tool_get_random_headers()
                )
            response_status = response.status
        except:
            return False
        if response_status == 503:
            return False
        temp = await response.json()
        if response_status == 200 and temp.get("origin"):
            return True
        else:
            return False


    async def __timer_check(self):
        if len(self.__pool) != 0:
            proxy_num = self.get_proxy_num()
            tasks = [self.__check_available(item) for item in self.__pool]
            # print(tasks)
            done = await asyncio.gather(*tasks)
            # print(tasks)
            # print(done)
            for _i in range(proxy_num):
                if done[_i] == False:
                    self.__pool[_i].points -= 1
                else:
                    self.__pool[_i].points += 2
        else:
            print('proxy pool is None')

        self.__evaluate_pool()

    def __drive_timer_check(self):
        # while True:
        asyncio.run(self.__timer_check())
        # time.sleep(self.__check_interval)
        thread = threading.Timer(self.__check_interval, self.__drive_timer_check)
        thread.start()

    def get_proxy_num(self):
        # print(self.__proxy)
        return len(self.__pool)

    def __drive_timer_spider(self):
        asyncio.run(self.__process_first_html())
        thread = threading.Timer(self.__spider_interval, self.__drive_timer_spider)
        thread.start()

    def __print_status(self):
        info = f"""
        pool_num = {self.get_proxy_num()}
        """
        print(info)
        thread = threading.Timer(self.__print_interval, self.__print_status)
        thread.start()

    def start_work(self):
        thread_spider = threading.Thread(target=self.__drive_timer_spider)
        thread_check = threading.Thread(target=self.__drive_timer_check)
        thread_print = threading.Thread(target=self.__print_status)

        thread_spider.start()
        thread_check.start()
        thread_print.start()







if __name__ == '__main__':
    test = proxy_pool()
    # while True:
    #     print(test.get_proxy_num())
    #     time.sleep(15)
    # test._drive_timer_check()

    # hello = [0, 1, 2, 3]
    test.start_work()

    print('hhhhh')


