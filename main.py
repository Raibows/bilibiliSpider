import time
import csv
from biblibiliSpider import SpiderModule, ProcessRawModule

default_spider = SpiderModule.bilibili_spider()

#make your own rule to collect info
def export_to_csv(spider=default_spider, csv_path='bilibili_rank_data.csv', rank_type='origin'):
    video_category = list(spider.video_category.keys())
    video_category.remove('all')
    info = []
    head = ['0rank_type', '1video_type', '2video_id', '3ranking',
                 '4video_title', '5video_upload_time', '6video_length_time',
                 '7author_id', '8author_followers', '9author_following',
                 '10view', '11danmaku', '12reply', '13favorite', '14coin', '15share', '16like',
                 '17spider_time'
            ]
    info.append(head)

    for video_type in video_category:
        time.sleep(0.1)
        videos = spider.get_rank_video_info(rank_type=rank_type, video_type=video_type)[1:]
        print('getting {} {} {}'.format(rank_type, video_type, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        for temp in videos:
            video_info = [i for i in head]
            video_info[0] = temp[0]
            video_info[1] = temp[1]
            video_info[2] = temp[3]
            video_info[3] = temp[2]
            video_info[4] = temp[4]
            video_info[7] = temp[5]

            video_aid = video_info[2]
            author_mid = video_info[7]

            video_info[5] = spider.get_video_upload_time_info(video_aid)
            video_info[6] = spider.get_video_length_info(video_aid)

            author_info = ProcessRawModule.process_raw_user_info(author_mid)
            video_info[8] = author_info[1]
            video_info[9] = author_info[0]
            time.sleep(0.05)
            video_info[10:17] = ProcessRawModule.process_raw_video_info(video_aid)

            video_info[17] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            info.append(video_info)
            time.sleep(0.1)

    with open(csv_path, 'a+', encoding='utf-8', newline='') as file:
        print('exporting now !')
        writer = csv.writer(file)
        writer.writerows(info)
        print('done !{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))





if __name__ == '__main__':
    export_to_csv()