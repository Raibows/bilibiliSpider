'''
Masquerading Module
'''
import ToolBox
from Config import spider_config
import time
import requests
import socket
from Config import flaskserver_config
default_proxy_server_address = flaskserver_config.flaskserver_host + ':' + str(flaskserver_config.flaskserver_port)
import json


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
            html =  requests.get(url, headers=ToolBox.tool_get_random_headers(),
                                proxies={"http": "http://{}".format(proxy)})
            if html is None:
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


def mas_get_proxy_dict() -> dict or None:
    '''
    for ProxyPool Module
    :return:
    '''
    url = default_proxy_server_address + '/proxy/get_one/dict'
    res = requests.get(url).text
    if res == 'None':
        return None
    res = json.loads(res)
    return res

def mas_get_proxy_string() -> str or None:
    '''
    for ProxyPool Module
    :return:
    '''
    url = default_proxy_server_address + '/proxy/get_one/string'
    res = requests.get(url).text
    if res == 'None':
        return None
    return res


# def mas_get_html(url):
#     '''
#     not for async aiohttp
#     :param url:
#     :return:
#     '''
#     retry_count = 5
#     proxy = mas_get_proxy_dict()
#     feedback_url = defalut_proxy_server_address + '/proxy/feedback'
#     feedback = proxy
#     while retry_count > 0:
#         try:
#             # print('hhh')
#             # print('proxy', proxy)
#             html = requests.get(
#                 url=url,
#                 headers=ToolBox.tool_get_random_headers(),
#                 proxies=proxy,
#             )
#             if html == None or html.status_code != 200:
#                 time.sleep(1)
#                 retry_count -= 1
#                 continue
#             #feedback increase
#             post_info = {
#                 'proxy': feedback,
#                 'flag': 'increase',
#             }
#             res = requests.post(
#                 url=feedback_url,
#                 data=post_info
#             )
#             log = 'mas_get_html feedback increase {} {} {}'.format(url, str(proxy), res.text)
#             ToolBox.tool_log_info(level='info', message=log)
#             print(log)
#             return html
#         except Exception as e:
#             log = 'mas_get_html error {} {}'.format(url, e)
#             ToolBox.tool_log_info(level='error', message=log)
#             print('mas_get_html error {}'.format(e))
#             retry_count -= 1
#     # retry_count == 0
#     # feedback
#     if proxy != None:
#         post_info = {
#             'proxy': feedback,
#             'flag': 'decrease',
#         }
#         res = requests.post(
#             url=feedback_url,
#             data=post_info
#         )
#         log = 'mas_get_html feedback decrease {} {} {}'.format(url, str(proxy), res.text)
#         ToolBox.tool_log_info(level='info', message=log)
#         print(log)
#     return None



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

    print(default_proxy_server_address)


    pass

# print(mas_get_proxy())
#
# print(get_host_ip())
