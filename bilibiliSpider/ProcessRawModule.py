'''
a module for processing json raw info to serialize info
'''
import time
from bilibiliSpider import SpiderModule

default_spider = SpiderModule.bilibili_spider()


def process_raw_video_info(aid, spider=default_spider):
    '''
    :param spider: an object of bilibili_spider
    :param aid:
    :return: list ['view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like']
    '''
    try:
        raw = spider.get_raw_video_info(aid)
    except Exception as e:
        print('{} {}'.format(e, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        raw = {'code': 0, 'message': '0', 'ttl': 1, 'data': {
            'aid': aid, 'view': -1, 'danmaku': -1, 'reply': -1, 'favorite': -1, 'coin': -1, 'share': -1, 'like': -1, 'now_rank': -1, 'his_rank': -1, 'no_reprint': -1, 'copyright': -1, 'argue_msg': '-1'
            }
               }
    info = []
    temp = ['0view', '1danmaku', '2reply', '3favorite', '4coin', '5share', '6like']
    for i in temp:
        info.append(raw.get('data').get(i[1:]))

    return info


def process_raw_user_info(mid, spider=default_spider):
    '''
    :param spider: an object of bilibili_spider
    :param mid: user's id
    :return: list ['following', 'follower']
    '''
    try:
        raw = spider.get_raw_user_info(mid)
    except Exception as e:
        print('{} {}'.format(e, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        raw = {
            'data' : {
                'following' : -1,
                'follower' : -1,
            }
        }
    info = []
    temp = ['0following', '1follower']
    for i in temp:
        info.append(raw.get('data').get(i[1:]))
    return info





