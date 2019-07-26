import requests
import ToolBox
import os
import time
import re


def get_html(url):
    response = requests.get(
        url=url,
        headers=ToolBox.tool_get_random_headers()
    )
    html = response.text

    return html


def limit(html: str) -> bool:
    res = re.findall('^-\d{2}', html)
    if res:
        print('res', res)
        return False
    else:
        return True

if __name__ == '__main__':
    base_url = r'https://www.kuaidaili.com/free/inha/{}/'

    for _i in range(1, 4):
        html = get_html(base_url.format(_i))
        time.sleep(0.893)
        if limit(html):
            print('yes')
        else:
            print('no')
