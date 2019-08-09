import Config
import requests
from bs4 import BeautifulSoup
import os
import time
import threading
import aiohttp
import asyncio
import ToolBox


default_check_interval = Config.proxypool_config.check_interval


class proxy_pool():
    def __init__(self):
        self.__proxy_urls = [
            r'https://www.kuaidaili.com/free/inha/{}/'
        ]
        self.__test_ip_url = 'http://httpbin.org/ip'
        self.__proxy = []
        self.__html_lib = None

        self.__check_interval = default_check_interval

        self.__timer = threading.Timer(1, self._drive_timer_check)
        self.__timer.start()

    def __first_get_html(self):
        html_lib = []
        for _i in range(1, 2):
            page_url = self.__proxy_urls[0].format(_i)
            print(page_url)
            html = requests.get(page_url, timeout=3)
            if html.status_code == 200:
                html_lib.append(html.text)
                time.sleep(1)

        self.__html_lib = html_lib

    async def __check_available(self, proxy):
        print(f'checking {proxy}')
        try:
            proxy = f'http://{proxy}'
            async with aiohttp.ClientSession() as session:
                response = await session.get(
                    url=self.__test_ip_url,
                    proxy=proxy,
                    timeout=5,
                    headers=ToolBox.tool_get_random_headers()
                )
            print(response.status)
        except:
            return False
        if response.status == 503:
            return False
        temp = await response.json()
        if response.status == 200 and temp.get("origin"):
            return True
        return False

    def _get_proxy(self):
        self.__first_get_html()
        for html in self.__html_lib:
            soup = BeautifulSoup(html, features="html5lib")
            ips = soup.find_all(
                    'td',
                    {
                        'data-title':'IP'
                    }
                 )
            ports = soup.find_all(
                'td',
                {
                    'data-title':'PORT'
                }
            )
            # os._exit(-1)
            proxies = zip(ips, ports)
            for item in proxies:
                proxy = item[0].string + ':' + item[1].string
                # if self.__check_available(proxy):
                self.__proxy.append(proxy)
            # self.__drive_timer_check()


    async def __timer_check(self):
        if len(self.__proxy) != 0:
            proxy_num = self.get_proxy_num()
            tasks = [self.__check_available(item) for item in self.__proxy]
            # print(tasks)
            done = await asyncio.gather(*tasks)
            # print(tasks)
            # print(done)
            for _i in range(proxy_num):
                if done[_i] == False:
                    del self.__proxy[_i]
        else:
            print('proxy pool is None')

    def _drive_timer_check(self):
        # while True:
        asyncio.run(self.__timer_check())
        # time.sleep(self.__check_interval)
        thread = threading.Timer(self.__check_interval, self._drive_timer_check)
        thread.start()

    def get_proxy_num(self):
        # print(self.__proxy)
        return len(self.__proxy)






if __name__ == '__main__':
    import requests

    url = 'http://httpbin.org/ip'
    url = 'https://www.bilibili.com/'
    ip = '39.97.50.177:6677'
    # ip = '47.89.37.177:3128'
    res = requests.get(
        headers=ToolBox.tool_get_random_headers(),
        url=url,
        proxies={
            'http': "http://{}".format(ip)
        }
    )
    print(res.text)
    pass
    # test = proxy_pool()
    # test._get_proxy()
    # while True:
    #     print(test.get_proxy_num())
    #     time.sleep(15)
    # test._drive_timer_check()

    # hello = [0, 1, 2, 3]


