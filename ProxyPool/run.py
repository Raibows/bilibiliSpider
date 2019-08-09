import sys
sys.path.append('..')
sys.path.append('.')

import ProxyPool

if __name__ == '__main__':
    pool = ProxyPool.proxy_pool()
    pool.start_work()