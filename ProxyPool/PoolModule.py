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
default_coroutines_semaphore = proxypool_config.coroutines_semaphore
default_evaluate_interval = proxypool_config.evaluate_interval

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
        #http://icanhazip.com/ #another test ip
        self.__pool = []
        self.__html_lib = None

        self.__check_interval = default_check_interval
        self.__spider_interval = default_spider_interval
        self.__print_interval = default_print_interval
        self.__evaluate_interval = default_evaluate_interval

        self.__db = ProxyPool.DatabaseModule.database()

        self.__semaphore = asyncio.Semaphore(default_coroutines_semaphore) #limit the number of coroutines

    async def __get_html(self, url):
        async with self.__semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()


    def __evaluate_pool(self):
        feedback = self.__db.get_feedback()
        increase_proxies = feedback.get('increase')
        decrease_proxies = feedback.get('decrease')

        for proxy in self.__pool:
            if proxy.get_string_address() in increase_proxies:
                proxy.points += 1
            elif proxy.get_string_address() in decrease_proxies:
                proxy.points -= 2

        delete_proxies = []
        add_proxies = []
        for proxy in self.__pool:
            if proxy.points < -3:
                self.__pool.remove(proxy)
                delete_proxies.append(proxy)
                print(f'Delete {proxy}')
            elif proxy.points > 1:
                add_proxies.append(proxy)
                print(f'Add {proxy}')
            else:
                print(proxy.get_string_address(), proxy.points)
        self.__db.delete_proxies(delete_proxies)
        self.__db.add_proxies(add_proxies)
        print('Evaluate done!' ,ToolBox.tool_get_current_time())
        thread = threading.Timer(self.__evaluate_interval, self.__evaluate_pool)
        thread.start()


    async def __process_first_html(self):
        tasks = [self.__get_html(self.__proxy_urls[0].format(_i)) for _i in range(1, 4)]
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
            async with self.__semaphore:
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
        try:
            temp = await response.json()
            if response_status == 200 and temp.get("origin"):
                return True
            else:
                return False
        except:
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
                    self.__pool[_i].points -= 3
                else:
                    self.__pool[_i].points += 3
        else:
            print('proxy pool is None')


    def __drive_timer_check(self):
        # while True:
        asyncio.run(self.__timer_check())
        # time.sleep(self.__check_interval)
        print('Check done!', ToolBox.tool_get_current_time())
        thread = threading.Timer(self.__check_interval, self.__drive_timer_check)
        thread.start()

    def get_proxy_num(self):
        # print(self.__proxy)
        return len(self.__pool)

    def __drive_timer_spider(self):
        asyncio.run(self.__process_first_html())
        print('Spider done!', ToolBox.tool_get_current_time())
        thread = threading.Timer(self.__spider_interval, self.__drive_timer_spider)
        thread.start()

    def __print_status(self):
        info = f'pool_num:{self.get_proxy_num()}  database_num:{self.__db.get_num()}'
        print(info, ToolBox.tool_get_current_time())
        thread = threading.Timer(self.__print_interval, self.__print_status)
        thread.start()

    def start_work(self):
        thread_spider = threading.Thread(target=self.__drive_timer_spider)
        thread_check = threading.Thread(target=self.__drive_timer_check)
        thread_evaluate = threading.Thread(target=self.__evaluate_pool)
        thread_print = threading.Thread(target=self.__print_status)



        thread_spider.start()
        thread_check.start()
        thread_evaluate.start()
        thread_print.start()







if __name__ == '__main__':
    test = proxy_pool()
    # while True:
    #     print(test.get_proxy_num())
    #     time.sleep(15)
    # test._drive_timer_check()

    # hello = [0, 1, 2, 3]
    test.start_work()



