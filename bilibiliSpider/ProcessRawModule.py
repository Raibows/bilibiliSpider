'''
a module for processing json raw info to serialize info
'''
from bilibiliSpider import SpiderModule
from bilibiliSpider import ToolModule

default_spider = SpiderModule.bilibili_spider()


def process_raw_video_info(aid, spider=default_spider):
    '''
    :param spider: an object of bilibili_spider
    :param aid:
    :return: list ['view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like']
    '''
    try:
        raw = spider.get_raw_video_info(aid)
        if raw.get('data') == None:
            raw = {'code': 0, 'message': '0', 'ttl': 1, 'data': {
                'aid': aid, 'view': -1, 'danmaku': -1, 'reply': -1, 'favorite': -1, 'coin': -1, 'share': -1, 'like': -1,
                'now_rank': -1, 'his_rank': -1, 'no_reprint': -1, 'copyright': -1, 'argue_msg': '-1'
            }
                }
    except Exception as e:
        log = 'ERROR IN process raw video info aid {} {}'.format(aid, e)
        ToolModule.tool_log_info(level='error', message=log)
        print(log)
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
        log = 'ERROR IN GET RAW USER INFO mid{} {}'.format(mid, e)
        ToolModule.tool_log_info(level='error', message=log)
        print(log)
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





