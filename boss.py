import os

from proxy import proxy
from crawl import spider
from crawl import db

class Boss:
    ''' 配置类
    '''
    pwd       = os.getcwd()
    html      = pwd + '/html/'
    proxy_txt = pwd + '/proxy.txt'
    boss_db   = pwd + '/boss.db'
    key_word  = 'php'


if __name__ == '__main__':
    # 获取代理ip
    proxy = proxy.Proxy(Boss.html, Boss.proxy_txt)
    proxy = proxy.run()

    # 开始爬取
    spider = spider.Spider(Boss.key_word, proxy, Boss.boss_db)
    spider.run()
