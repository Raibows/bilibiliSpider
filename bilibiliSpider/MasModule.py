'''
Masquerading Module
'''
import ToolBox
import bilibiliSpider
from Config import spider_config
import time
import requests
from fake_headers import Headers
import socket



headers= Headers(browser='Chrome')

#set your own proxy pool address, default is localhost port 5010
_ip_proxy_pool_addr = spider_config.mas_proxy_pool_ip


def mas_get_proxy():
    return requests.get("http://{}/get/".format(_ip_proxy_pool_addr)).content #get proxy

def mas_delete_proxy(proxy):
    requests.get("http://{}/delete/?proxy={}".format(_ip_proxy_pool_addr, proxy))

def mas_get_html(url):
    # ....
    retry_count = 5
    proxy = mas_get_proxy()
    proxy = proxy.splitlines()
    while retry_count > 0:
        try:
            # print('hhh')
            # print('proxy', proxy)
            html =  requests.get(url, headers=headers.generate(),
                                proxies={"http": "http://{}".format(proxy)})
            if html == None:
                time.sleep(1)
                continue
            # 使用代理访问
            return html
        except Exception as e:
            log = 'mas_get_html error {} {}'.format(url, e)
            ToolBox.tool_log_info(level='error', message=log)
            print('mas_get_html error {}'.format(e))
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    # print('zzzz', html)
    mas_delete_proxy(proxy)
    return None

def mas_get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip





if __name__ == '__main__':
    pass

# print(mas_get_proxy())
#
# print(get_host_ip())
