from fake_headers import Headers
import requests
import json
import sys
import os
import urllib
from bs4 import BeautifulSoup
import re
import time




class bilibili_spider():
    def __init__(self):
        self.api_video_info = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}' #video aid
        self.api_user_info = 'https://api.bilibili.com/x/relation/stat?vmid={}' #user mid
        self.api_rank = 'https://www.bilibili.com/ranking/{}/{}' #rank category, video category
        self.api_video_html = 'https://www.bilibili.com/video/av{}/' #video aid
        self.video_category = {
            'all': '0',
            'animation': '1',
            'guochuang': '168',
            'music': '3',
            'dance': '129',
            'game': '4',
            'technology': '36',
            'digital': '188',
            'life': '160',
            'guichu': '119',
            'fashion': '155',
            'entertainment': '5',
            'movie': '181',
        }
        self.rank_category = {
            'all' : 'all',
            'origin' : 'origin'
        }
        self.rank_time_category = {
            'day' : '/0/1/',
            'three_days' : '/0/3/',
            'week' : '/0/7/',
            'month' : '/0/30/'
        }
    def get_random_headers(self, browser='Chrome'):
        '''
        :return:random headers
        '''
        headers = Headers(browser=browser)
        temp = headers.generate()
        return temp

    def get_raw_video_info(self, aid):
        '''
        :param aid: video's aid
        :return: dict, this video's raw info
        '''
        url = self.api_video_info.format(aid)
        res = requests.get(url, headers=self.get_random_headers())
        res_dict = res.json()
        return res_dict

    def get_raw_user_info(self, mid):
        '''
        :param mid: users' mid
        :return: dict, this user's raw info
        '''
        url = self.api_user_info.format(mid)
        res = requests.get(url, headers=self.get_random_headers())
        res_dict = res.json()
        return res_dict

    def get_video_length_info(self, aid):
        '''
        :param aid:
        :return: the time length of a video, unit: seconds
        '''
        url = self.api_video_html.format(aid)
        res = requests.get(url, headers=self.get_random_headers())
        res = res.text
        error_flag = '<div class="error-text">啊叻？视频不见了？</div>'
        if error_flag in res:
            return -1
        video_time = re.findall(r'\"timelength\":\d+', res)[0]
        video_time = re.findall(r'\d+', video_time)[0]
        video_time = int(eval(video_time) / 1000)
        return video_time

    def get_video_upload_time_info(self, aid):
        '''

        :param aid:
        :return: the upload time of a video, exp 2019-06-29 16:59:30
        '''
        url = self.api_video_html.format(aid)
        res = requests.get(url, headers=self.get_random_headers())
        res = res.text
        error_flag = '<div class="error-text">啊叻？视频不见了？</div>'
        if error_flag in res:
            return -1
        try:
            upload_time = re.findall(r'\"uploadDate\" content=\"\d+-\d+-\d+\s+\d+:\d+:\d+\">', res)[0]
            upload_time = re.findall(r'\d+-\d+-\d+\s+\d+:\d+:\d+', upload_time)[0]
        except Exception as e:
            print(aid)
            print('{} {}'.format(e, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            upload_time = re.findall(r'\"time\":\"\d+-\d+-\d+\s+\d+:\d+:\d+\",', res)[0]
            upload_time = re.findall(r'\d+-\d+-\d+\s+\d+:\d+:\d+', upload_time)[0]
        return upload_time


    def get_rank_video_info(self, rank_type='origin', video_type='all', rank_time_type='day'):
        '''
        :param video_type: string, the category of rank, default is origin, the category
        of the video is all
        :return: list, ['video_rank', 'video_aid', 'video_title', 'up_mid']
        '''
        info = []
        info.append(['0rank_type', '1video_type', '2video_rank', '3video_aid', '4video_title', '5up_mid'])

        suffix = self.rank_time_category.get(rank_time_type)
        try:
            url = self.api_rank.format(self.rank_category.get(rank_type), self.video_category.get(video_type)) + suffix
        except Exception as e:
            print('{} {}'.format(e, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            print('ERROR IN {} VIDEO_TYPE={}'.format(sys._getframe().f_code.co_name, video_type))
            os._exit(-1)
        else:
            res = urllib.request.Request(url, headers=self.get_random_headers())
            html = urllib.request.urlopen(res).read().decode('utf-8')
            soup = BeautifulSoup(html, features='html5lib')
            points = soup.find_all('div',
                                   {'class' : 'pts'})
            titles = soup.find_all('a',
                                   {'class' : 'title', 'target': '_blank'})
            author_ids = soup.find_all('a',
                                       target= '_blank',
                                       href=re.compile('//space.bilibili.com/'))


            # print(titles)
            # os._exit(-1)

            for i in range(len(points)):
                aid = re.findall(r'av\d+/', str(titles[i]))
                aid = aid[0][2:-1]

                up_mid = re.findall(r'//space.bilibili.com/\d+', str(author_ids[i]))
                up_mid = re.findall(r'\d+', up_mid[0])[0]

                title = re.findall(r'>[\S\s]+<', str(titles[i]))
                title = title[0][1:-1]

                info.append([rank_type, video_type, i+1, aid, title, up_mid])
            return info



# test_aid = 57645778
# test_aid = 55406216
# test = bilibili_spider()
# # x = test.get_video_upload_time_info(57649778)
# # # x = test.get_raw_video_info(19308734)
# # # x = test.get_raw_video_info(19308734)
# x = test.get_raw_video_info(test_aid)
# print(x)

