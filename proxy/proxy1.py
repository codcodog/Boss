import queue
import time
import random
import threading
import sys

import requests
from bs4 import BeautifulSoup

class Proxy1:
    def __init__(self):
        '''
        @param  获取的代理队列
        @param  获取的代理数, 至少满足
        @param  可用的proxy队列
        @param  爬取到proxy的总数
        '''
        self.proxy           = queue.Queue()
        self.num             = 300
        self.available_proxy = queue.Queue()
        self.size            = 0

    def crawl_proxy(self):
        ''' 爬取高匿代理
        '''
        print('########## 爬取高匿代理 #############')
        url_template  = 'http://www.kuaidaili.com/free/inha/%s/'
        page = 1

        while (not self.proxy.qsize() > self.num):
            url = url_template % page
            header = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
            }
            html = requests.get(url, headers = header).content.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')

            div_res = soup.find_all('div', id = 'list')
            tr_res = div_res[0].find_all('tr')

            # 删除第一个没用的表头信息
            del tr_res[0]

            # 解释文本, 获取代理
            for tr in tr_res:
                td_res = tr.find_all('td')

                ip           = td_res[0].string
                port         = td_res[1].string
                protocol_tmp = td_res[3].string
                protocol     = str(protocol_tmp).lower()
                proxy        = protocol + '://' + ip + ':' + port

                self.proxy.put(proxy)

            print('爬取高匿代理第%s页, 爬取到Proxy: %s' % (page, self.proxy.qsize()))
            page += 1
            time.sleep(random.randint(15, 30))
        else:
            self.size = self.proxy.qsize()
            print('爬取完成, 一共爬取了%s个\n' % self.proxy.qsize())


    def is_active(self, proxy):
        ''' 检测代理ip活性
        '''
        url        = 'https://www.zhipin.com/'
        protocol   = proxy.split(':')[0]
        test_proxy = {protocol: proxy}

        try:
            res = requests.get(url, proxies = test_proxy, timeout = 3)

            return res.status_code == 200
        except:
            return False

    def concurrent_test(self):
        ''' 并发测试proxy是否可用
        可用则写进proxy.txt文件
        '''
        while (not self.proxy.empty()):
            proxy = self.proxy.get()

            if (self.is_active(proxy)):
                self.available_proxy.put(proxy)

    def per(self):
        ''' 完成度
        '''
        status = 0
        while (True):
            if (self.proxy.empty()):
                msg = '检测Proxy可用性: {}/{}'.format(self.size, self.size)
                sys.stdout.write('\r'*status)
                sys.stdout.write(msg)
                sys.stdout.flush()
                break
            else:
                tested = self.size - self.proxy.qsize()
                msg = '检测Proxy可用性: {}/{}'.format(tested, self.size)

                sys.stdout.write('\r'*status)
                sys.stdout.write(msg)
                sys.stdout.flush()
                status = len(msg)
                time.sleep(0.1)

    def run(self):
        ''' 执行程序
        '''
        self.crawl_proxy()

        thread_num  = 20
        thread_list = []
        start_time  = time.time()

        print('########## 检测proxy活性 #############')
        # 检测proxy线程
        for i in range(thread_num):
            t = threading.Thread(target = self.concurrent_test)
            thread_list.append(t)

        for i in thread_list:
            i.start()

        # 主线程展示检测进度
        self.per()

        # 等待子线程全部结束
        for i in thread_list:
            i.join()

        end_time = time.time()
        t        = round(end_time - start_time)
        total    = self.available_proxy.qsize()
        print('\nProxy检测完成, {}个可用, 耗时{}s.'.format(total, t))

        # 取消写入proxy.txt文件, 直接返回queue对象
        # self.save_proxy()
        return self.available_proxy
