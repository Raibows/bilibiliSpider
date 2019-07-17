import requests
from bs4 import BeautifulSoup
import os
import time
import threading



class proxy_pool():
    def __init__(self):
        self.__proxy_urls = [
            r'https://www.kuaidaili.com/free/inha/{}/'
        ]
        self.__test_ip_url = 'http://httpbin.org/ip'
        self.__proxy = []
        self.__html_lib = None

        self.__timer = threading.Timer(1, self.__timer_check)
        self.__timer.start()

    def __get_html(self):
        html_lib = []
        for url in self.__proxy_urls:
            for _i in range(1, 5):
                page_url = url.format(_i)
                print(page_url)
                html = requests.get(page_url, timeout=3)
                if html.status_code == 200:
                    html_lib.append(html.text)
                    time.sleep(1)

        self.__html_lib = html_lib

    def __check_available(self, proxy):
        print(f'checking {proxy}')
        try:
            html = requests.get(self.__test_ip_url, proxies={"http": "http://{}".format(proxy)}, timeout=3)
        except:
            return False
        if html.status_code == 200 and html.json().get("origin"):
            return True
        return False

    def _get_proxy(self):
        self.__get_html()
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
                if self.__check_available(proxy):
                    self.__proxy.append(proxy)


    def __timer_check(self):
        if len(self.__proxy) != 0:
            for proxy in self.__proxy:
                if not self.__check_available(proxy):
                    self.__proxy.remove(proxy)
        else:
            print('proxy pool is None')
        self.__timer = threading.Timer(10, self.__timer_check)
        self.__timer.start()




    def get_proxy_num(self):
        print(self.__proxy)
        return len(self.__proxy)






if __name__ == '__main__':
    # test = proxy_pool()
    # test._get_proxy()
    # test.get_proxy_num()
    proxy = '39.97.50.177:6677'
    test_url = r'https://www.bilibili.com/index/ding.json'
    test_ip_url = 'http://httpbin.org/ip'
    while True:
        res = requests.get(test_ip_url, proxies={"http": "http://{}".format(proxy)}, timeout=3)
        print(res.status_code)
        res = res.json()
        print(res.get('origin'))
        time.sleep(3)

