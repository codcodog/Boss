from proxy import proxy
from crawl import spider

if __name__ == '__main__':
    # 获取代理ip
    proxy = proxy.Proxy()
    proxy = proxy.run()

    # 开始爬取
    key_word = 'php'
    spider = spider.Spider(key_word, proxy)
    spider.run()
