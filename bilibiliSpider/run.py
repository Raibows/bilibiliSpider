import sys
sys.path.append('..')
sys.path.append('.')
import bilibiliSpider
from Config import spider_config






if __name__ == '__main__':
    print(spider_config())
    bilibiliSpider.process_run_main()



