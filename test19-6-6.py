import requests
import webbrowser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import requests, json
import threading
base_url = 'http://ncepu.xyz:5000/auth/login'
headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'zh-CN,zh;q=0.9'
         }
data = {'id' : 'test',
        'password' : '333',
        'submit': 'Login in'}

session = requests.session()

res = session.post(url=base_url, data=data, headers=headers)

res = session.get('http://ncepu.xyz:5000/')

print(res.text)





