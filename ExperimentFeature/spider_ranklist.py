'''
spider 100 ranking list from bilibili
'''
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import urllib
import json
import csv
import time
import os
from bilibiliSpider.SpiderModule import category, rank_types, headers



'''
Global params
csv_path is the local address to store the info in csv format
category is a multiple list to store different url identifiers for different types of videos
rank_types is a choice dict for total rank or origin rank 
'''

headers = Headers(browser='chrome')
csv_path = "bilibili_data.csv"
category = [
    ['0', 'all'],
    ['1', 'animation'],
    ['168', 'guochuang'],
    ['3', 'music'],
    ['129', 'dance'],
    ['4', 'game'],
    ['36', 'technology'],
    ['188', 'digital'],
    ['160', 'life'],
    ['119', 'guichu'],
    ['155', 'fashion'],
    ['5', 'entertainment'],
    ['181', 'movie']
]
rank_types = {
    'all': 'https://www.bilibili.com/ranking/all/',
    'origin': 'https://www.bilibili.com/ranking/origin/'
}






'''
Global params
database is the temp dict to store every video raw info
points_data is the temp list to store every video points
av_data is the temp list to store every video avid
'''

database = {}
points_data = []
av_data = []


def initial_all():
    '''
    init the database, points_data, av_data
    :return:
    '''
    global database
    global points_data
    global av_data
    database = {}
    points_data = []
    av_data = []

def create_base_url(type, index=0):
    '''
    get different rank url through choosing from
    rank_types dict and category list
    :param type: string, shall be an element from rank_types dict
    :param index: int, will choose category list through index
    :return: string, url
    '''
    suffix = '/0/3/'
    if rank_types.get(type) is None:
        print('ERROR, TYPE NOT FOUND !')
        os._exit(-1)
    else:
        url = rank_types[type] + category[index][0] + suffix
        print('got rank {} {} url'.format(type, category[index][1]))
        return url

def get_html(url):
    '''
    get html from url
    :param url: shall be a url
    :return: a html
    '''
    try:
        res = urllib.request.Request(url, headers=headers.generate())
        html = urlopen(res).read().decode('utf-8')
    except:
        print('ERROR in get_html {}'.format(url))
        os._exit(-1)
    return html

def get_rawinfo(soup):
    '''
    through beautiful soup to find specific info
    :param soup:
    :return: useful raw info
    '''
    temp = soup.find_all('div',
                         {'class':'pts'})
    for item in temp:
        points = re.findall(r'\d+', str(item))
        points_data.append(points[0])
    return soup.find_all('a',
                         {'class': 'title',
                          'target': '_blank'})


def get_av(raw):
    '''
    get a video's avid from raw info
    :param raw: shall be the return of func get_rawinfo
    :return: avid
    '''
    av = re.findall(r'av\d+/', str(raw))
    temp = str(av[0][2:-1])
    print('got av {}'.format(temp))
    av_data.append(temp)
    return temp


def get_json(av):
    '''
    get all useful info of a video through the video's avid
    :param av: string, avid
    :return: dict, useful info
    '''
    base = "https://api.bilibili.com/x/web-interface/archive/stat?aid="
    url = base + av
    try:
        res = urllib.request.Request(url,headers={'User-Agent': 'Chrome'})
        html = urlopen(res).read().decode('utf-8')
    except:
        print('ERROR in get_json {}'.format(url))
        os._exit(-1)
    return json.loads(html)


def extract_tidy(raw_data, rank):
    '''
    to format the all raw data
    :param raw_data: shall be the return of func get_rawinfo
    :param rank: int, from 1 to 100
    :return: formatted info of a video
    '''
    database[rank] = [
        raw_data['data']['view'],
        raw_data['data']['danmaku'],
        raw_data['data']['reply'],
        raw_data['data']['favorite'],
        raw_data['data']['coin'],
        raw_data['data']['share'],
        raw_data['data']['like']
    ]



def export_to_csv(csvpath=csv_path):
    '''
    write the result data in csv
    default is a+ model
    :param csvpath: the csv path
    :return:
    '''
    print('exporting data to csv now !')
    now = time.strftime('%Y-%m-%d', time.localtime())
    with open(csvpath, "a+", encoding='utf-8', newline='') as mycsvfile:
        writer = csv.writer(mycsvfile)
        writer.writerow([now])
        writer.writerow(['rank', 'view', 'danmu', 'reply', 'favorite', 'coin', 'share', 'like', 'points', 'avid'])
        for i in range(100):
            temp = database[i+1]
            temp.insert(0, i+1)
            temp.append(points_data[i])
            temp.append(av_data[i])
            writer.writerow(temp)



if __name__ == '__main__':
    rank_type = 'origin'
    category_num = len(category)
    for i in range(1, category_num):
        initial_all()
        base_url = create_base_url(rank_type, i)
        html = get_html(base_url)
        soup = BeautifulSoup(html)
        all_raw_info = get_rawinfo(soup)
        for index,item in enumerate(all_raw_info, start=1):
            av = get_av(item)
            time.sleep(0.1)
            origin_data = get_json(av)
            time.sleep(0.2)
            extract_tidy(origin_data, index)
        export_to_csv()
        print('rank {} category {} has done !'.format(rank_type, category[i][1]))



