from Config import proxypool_config
import ProxyPool
from bs4 import BeautifulSoup
import threading
import aiohttp
import asyncio
import ToolBox
import time
import re



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
            r'https://www.kuaidaili.com/free/inha/{}/',
            [r'http://www.iphai.com/free/ng', r'http://www.iphai.com/free/wg'],
            r'http://ip.jiangxianli.com/?page={}',
            r'https://proxy-list.org/english/index.php?p={}',
            r'http://www.66ip.cn/nmtq.php?getnum={}',
            r'http://www.ip3366.net/free/?stype=1&page={}',
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
        proxy = self.__db.get_one_string()
        # print('hhhhhhhhhhhh', proxy)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url,
                    headers=ToolBox.tool_get_random_headers(),
                    proxy=proxy,
                ) as response:
                    return await response.text()
        except Exception as e:
            print(f'ERROR IN GET {url} {e}')
            return []


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
                # print(proxy.get_string_address(), proxy.points)
                pass
        self.__db.delete_proxies(delete_proxies)
        self.__db.add_proxies(add_proxies)
        print('Evaluate done!' ,ToolBox.tool_get_current_time())
        thread = threading.Timer(self.__evaluate_interval, self.__evaluate_pool)
        thread.start()


    async def __process_first_html(self):
        # tasks = [self.__get_html(self.__proxy_urls[0].format(_i)) for _i in range(1, 4)]
        page_count = 4
        done = []
        for _i in range(1, page_count):
            url = self.__proxy_urls[0].format(_i)
            html = await self.__get_html(url)
            done.append(html)
            time.sleep(1.148)
        # done = await asyncio.gather(*tasks)
        for html in done:
            if html:
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
                # print(len(ips))
                # os._exit(-1)
                for item in proxies:
                    proxy = ProxyPool.proxy(item[0].string, item[1].string)
                    if proxy not in self.__pool:
                        self.__pool.append(proxy)
                        print(f'process_first_html got {proxy.get_string_address()}')
            #     print('here', self.get_proxy_num())
            # print('final ', self.get_proxy_num())
            # os._exit(-1)


    async def __process_second_html(self):
        urls = self.__proxy_urls[1]
        tasks = [self.__get_html(url) for url in urls]
        done = await asyncio.gather(*tasks)
        for res in done:
            if res:
                soup = BeautifulSoup(res, features='html5lib')
                ipandport = soup.find_all('td')
                for i, ip in enumerate(ipandport):
                    temp = re.findall('\d+\.\d+\.\d+\.\d+', ip.string)
                    if temp:
                        port = ipandport[i+1].string
                        port = port.strip()
                        new = ProxyPool.proxy(temp[0], port)
                        if new not in self.__pool:
                            self.__pool.append(new)
                            print(f'process_second_html got {new.get_string_address()}')


    async def __process_third_html(self):
        page_count = 2
        urls = [self.__proxy_urls[2].format(_i+1) for _i in range(page_count)]
        tasks = [self.__get_html(url) for url in urls]
        done = await asyncio.gather(*tasks)
        for html in done:
            if html:
                soup = BeautifulSoup(html, features='html5lib')
                res = soup.find_all(
                    'td'
                )
                for _i, item in enumerate(res):
                    str_ = str(item.string)
                    temp = re.findall('\d+\.\d+\.\d+\.\d+', str_)
                    if temp:
                        ip = temp[0]
                        port = res[_i+1].string
                        port = str(port)
                        port = port.strip()
                        new = ProxyPool.proxy(ip, port)
                        if new not in self.__pool:
                            self.__pool.append(new)
                            print(f'process_third_html got {new.get_string_address()}')

    async def __process_fourth_html(self):
        '''
        foreign website
        :return:
        '''
        page_count = 6
        urls = [self.__proxy_urls[3].format(_i+1) for _i in range(page_count)]
        tasks = [self.__get_html(url) for url in urls]
        done = await asyncio.gather(*tasks)
        import base64
        for html in done:
            proxies = re.findall(r"Proxy\('(.*?)'\)", html)
            for proxy in proxies:
                temp = base64.b64decode(proxy).decode()
                ip = re.findall('\d+\.\d+\.\d+\.\d+', temp)
                ip = ip[0]
                port = re.findall(':\d+', temp)
                port = port[0]
                port = port[1:]
                new = ProxyPool.proxy(ip, port)
                if new not in self.__pool:
                    self.__pool.append(new)
                    print(f'process_fourth_html got {new.get_string_address()}')

    async def __process_fifth_html(self):
        '''
        forbidden website
        :return:
        '''
        proxy_count = 20
        url = self.__proxy_urls[4].format(proxy_count)
        html = await self.__get_html(url)
        print(html)
        items = re.findall('\d+\.\d+\.\d+\.\d+:\d{1,5}', html)
        for item in items:
            ip = re.findall('\d+\.\d+\.\d+\.\d+', item)
            ip = ip[0]
            port = item.replace(ip, "")
            port = port[1:]
            new = ProxyPool.proxy(ip, port)
            if new not in self.__pool:
                self.__pool.append(new)
                print(f'process_fifth_html got {new.get_string_address()}')

    async def __process_sixth_html(self):
        page_count = 5
        urls = [self.__proxy_urls[5].format(_i+1) for _i in range(page_count)]
        tasks = [self.__get_html(url) for url in urls]
        done = await asyncio.gather(*tasks)
        for html in done:
            if html:
                soup = BeautifulSoup(html, features='html5lib')
                ipandport = soup.find_all('td')
                for i, ip in enumerate(ipandport):
                    temp = re.findall('\d+\.\d+\.\d+\.\d+', ip.string)
                    if temp:
                        port = ipandport[i+1].string
                        port = port.strip()
                        new = ProxyPool.proxy(temp[0], port)
                        if new not in self.__pool:
                            self.__pool.append(new)
                            print(f'process_sixth_html got {new.get_string_address()}')





    async def __check_available(self, proxy:ProxyPool.proxy):
        proxy = proxy.get_string_address()
        print(f'checking {proxy}')
        try:
            # async with semaphore:
            async with aiohttp.ClientSession() as session:
                response = await session.get(
                    url=self.__test_ip_url,
                    proxy=proxy,
                    timeout=default_check_proxy_timeout,
                    headers=ToolBox.tool_get_random_headers()
                )
            response_status = response.status
        except Exception as e:
            print(proxy, '11111111111111111', e)
            return (proxy, False)
        if response_status == 503:
            print(proxy, '22222222222222222')
            return (proxy, False)
        try:
            temp = await response.json()
            if response_status == 200 and temp.get("origin"):
                return (proxy, True)
            else:
                print(proxy, '3333333333333333')
                return (proxy, False)
        except Exception as e:
            print(proxy, '4444444444444444444', e)
            return (proxy, False)


    async def __timer_check(self):
        if self.get_proxy_num() != 0:
            tasks = [self.__check_available(item) for item in self.__pool]
            done = await asyncio.gather(*tasks)
            # done = await asyncio.wait(tasks)
            mark_up = []
            mark_down = []
            for item in done:
                if item[1]:
                    mark_up.append(item[0])
                else:
                    mark_down.append(item[0])
            for proxy in self.__pool:
                str_ = proxy.get_string_address()
                if str_ in mark_up:
                    proxy.points += 3
                elif str_ in mark_down:
                    proxy.points -= 3
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

    async def __timer_spider(self):
        tasks = [
            self.__process_first_html(),
            self.__process_second_html(),
            self.__process_third_html(),
            # self.__process_fourth_html(),
            # self.__process_fifth_html(),
            self.__process_sixth_html(),
        ]
        await asyncio.gather(*tasks)

    def __drive_timer_spider(self):
        asyncio.run(self.__timer_spider())
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
        time.sleep(30)
        thread_check.start()
        thread_evaluate.start()
        thread_print.start()







if __name__ == '__main__':
    test = proxy_pool()
    test.start_work()
    url = 'http://www.66ip.cn/nmtq.php?getnum=20'
    # url = r'https://www.kuaidaili.com/free/inha/1/'
    # import requests
    # import ToolBox
    # html = requests.get(url, headers=ToolBox.tool_get_random_headers())
    # print(html.text)


