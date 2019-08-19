import bilibiliSpider
import requests
import sys
import os
from bs4 import BeautifulSoup
import re
import time
import ToolBox
import multiprocessing
import ast

class bilibili_spider():
    def __init__(self):
        self.api_video_info = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}' #video aid
        self.api_user_info = 'https://api.bilibili.com/x/relation/stat?vmid={}' #user mid
        self.api_rank = 'https://www.bilibili.com/ranking/{}/{}' #rank category, video category
        self.api_video_html = 'https://www.bilibili.com/video/av{}/' #video aid
        self.api_latest_video = 'https://api.bilibili.com/x/web-interface/newlist?&rid={}&pn={}&ps={}' #3 params
        self.mas_proxy_flag = False  # ip proxy default is false
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
        self.video_rid_category = {
            'animation' : [24, 27, 25, 47, 86],
            'guochuang' : [168, 169, 170, 153, 195],
            'music' : [31, 29, 59, 30, 130, 28],
            'dance' : [154, 20, 156],
            'game' : [171, 17, 65, 172, 121, 136],
            'technology' : [39, 124, 122, 96, 98, 176],
            'digital' : [95, 189, 190, 191],
            'life' : [138, 21, 75, 76, 161, 162, 163, 174],
            'guichu' : [22, 26, 126, 127],
            'fashion' : [157, 158, 159, 164, 192],
            'entertainment' : [71, 137, 131],
            'movie' : [182, 183, 184, 85]
         }
        self.__error = []
        self.__lock = multiprocessing.Lock()

    def __get_html_requests(self, url):
        if self.mas_proxy_flag:
            try_count = 0
            html = bilibiliSpider.mas_get_html(url)
            while html is None:
                try_count += 1
                if try_count == 3:
                    html = requests.get(url, headers=ToolBox.tool_get_random_headers())
                else:
                    html = bilibiliSpider.mas_get_html(url)
                time.sleep(1)
            return html
        else:
            return requests.get(url, headers=ToolBox.tool_get_random_headers())
    def __log_error(self, aid):
        self.__lock.acquire()
        if aid not in self.__error:
            self.__error.append(aid)
        self.__lock.release()

    def get_error_count(self):
        self.__lock.acquire()
        length = len(self.__error)
        self.__lock.release()
        return length


    def get_raw_video_info(self, aid):
        '''
        :param aid: video's aid
        :return: dict, this video's raw info
        '''
        url = self.api_video_info.format(aid)
        res = self.__get_html_requests(url)
        try_412 = 0
        while res.status_code == 412:
            if try_412 == 3:
                break
            else:
                try_412 += 1
                res = self.__get_html_requests(url)
                time.sleep(1)
        res_dict = res.json()
        return res_dict

    def get_raw_user_info(self, mid):
        '''
        :param mid: users' mid
        :return: dict, this user's raw info
        '''
        url = self.api_user_info.format(mid)
        res = self.__get_html_requests(url)
        res_dict = res.json()
        return res_dict

    def get_video_length_info(self, aid):
        '''
        :param aid:
        :return: the time length of a video, unit: seconds
        '''
        url = self.api_video_html.format(aid)
        res = self.__get_html_requests(url)
        res = res.text
        error_flag = '<div class="error-text">啊叻？视频不见了？</div>'
        if error_flag in res:
            self.__log_error(aid)
            return -1
        try:
            video_time = re.findall(r'\"timelength\":\d+', res)[0]
            video_time = re.findall(r'\d+', video_time)[0]
            video_time = int(ast.literal_eval(video_time) / 1000)
            # video_time = int(eval(video_time) / 1000)
        except:
            video_time = -1
            log = 'ERROR IN GETTING VIDEO LENGTH AID {}'.format(aid)
            ToolBox.tool_log_info(level='error', message=log)
            print(log)
        return video_time

    def get_video_upload_time_info(self, aid):
        '''

        :param aid:
        :return: the upload time of a video, exp 2019-06-29 16:59:30
        '''
        url = self.api_video_html.format(aid)
        error_flag = '<div class="error-text">啊叻？视频不见了？</div>'
        try:
            res = self.__get_html_requests(url)
            res = res.text
        except Exception as e:
            log = 'ERROR in getting video upload time {} {}'.format(aid, e)
            ToolBox.tool_log_info(level='error', message=log)
            print(log)
            res = error_flag
        if error_flag in res:
            log = 'ERROR in getting video upload time {} {}'.format(aid, error_flag)
            ToolBox.tool_log_info(level='error', message=log)
            self.__log_error(aid)
            return -1
        try:
            upload_time = re.findall(r'\"uploadDate\" content=\"\d+-\d+-\d+\s+\d+:\d+:\d+\">', res)[0]
            upload_time = re.findall(r'\d+-\d+-\d+\s+\d+:\d+:\d+', upload_time)[0]
        except Exception as e:
            log = 'ERROR in getting video upload time {} {}'.format(aid, e)
            ToolBox.tool_log_info(level='error', message=log)
            print(log)
            upload_time = re.findall(r'\"time\":\"\d+-\d+-\d+\s+\d+:\d+:\d+\",', res)[0]
            upload_time = re.findall(r'\d+-\d+-\d+\s+\d+:\d+:\d+', upload_time)[0]
        return upload_time

    def get_latest_video_info(self, rid, ps=1, pn=50):
        '''
        :param rid: the video category code, you could see them in rid_appendix.txt
        :param ps: the page number of latest, default is the first page
        :param pn: the size of page, default is 50, no more than 50
        :return:
        '''

    def get_rank_video_info(self, rank_type='origin', video_type='all', rank_time_type='day'):
        '''
        :param video_type: string, the category of rank, default is origin, the category
        of the video is all
        :return: list, ['video_rank', 'video_aid', 'video_title', 'up_mid']
        '''
        info = []
        info.append(['0rank_type', '1video_type', '2video_rank', '3video_aid', '4video_title', '5up_mid', '6points'])

        suffix = self.rank_time_category.get(rank_time_type)
        try:
            url = self.api_rank.format(self.rank_category.get(rank_type), self.video_category.get(video_type)) + suffix
        except Exception as e:
            log = 'ERROR IN {} VIDEO_TYPE={} {}'.format(sys._getframe().f_code.co_name, video_type, e)
            ToolBox.tool_log_info(level='error', message=log)
            print(log)
            os._exit(-1)
        else:
            # res = urllib.request.Request(url, headers=self.get_random_headers())
            # html = urllib.request.urlopen(res).read().decode('utf-8')
            res = self.__get_html_requests(url)
            html = res.text
            # os._exit(-1)
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

                point = re.findall(r'\d+', str(points[i]))
                point = point[0]

                info.append([rank_type, video_type, i+1, aid, title, up_mid, point])
            return info

    def get_rid_category(self, port_begin=2, port_end=200):
        '''
        :param port_begin: =0 or 1, return all latest video categories videos
        :param port_end:
        :return: [{rid,tname}]
        '''
        info = []
        for i in range(port_begin, port_end):
            try:
                ToolBox.tool_stop_random_time(0.1, 0.25)
                url = self.api_latest_video.format(i, 1, 1)
                res = self.__get_html_requests(url)
                res_dict = res.json()
                if res_dict['data']['page']['count'] > 0:
                    tname = res_dict['data']['archives'][0]['tname']
                    if tname == '':
                        continue
                    print(i, tname)
                    info.append({
                        'rid' : i,
                        'tname' : tname
                    })
            except Exception as e:
                print(e)
                print(i, 'end')
                break
        return info




if __name__ == '__main__':

    # test_aid = 57721760
    # test_aid = 55406216
    test = bilibili_spider()
    # x = test.get_video_upload_time_info(57649778)
    # # x = test.get_raw_video_info(19308734)
    # # x = test.get_raw_video_info(19308734)
    # x = test.get_raw_video_info(test_aid)
    # x = test.get_video_upload_time_info(test_aid)

    # test.mas_proxy_flag = True
    # x = test.get_video_length_info(test_aid)
    # print(x)
    # test = bilibili_spider()
    # res = requests.get(url=test. .format(57721760), proxies={"http": "http://{}".format(proxy)})
    #
    # print(res.text)
    # a = test.get_raw_video_info(59037693)
    # print(a)
    # test.mas_proxy_flag = Config.spider_config.mas_proxy_flag
    # a = test._get_html_requests(r'https://api.bilibili.com/x/web-interface/archive/stat?aid=59037693')
    # print(a.json())