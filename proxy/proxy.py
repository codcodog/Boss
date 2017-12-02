import os
import queue
import threading
import time
import sys

import requests
from bs4 import BeautifulSoup

class Proxy:
    def __init__(self, html_path = None, proxy_file = None):
        # 基于项目Boss下执行的路径
        self.html_path       = html_path
        self.proxy_file      = proxy_file
        self.proxy           = queue.Queue()
        self.available_proxy = queue.Queue()
        self.size            = 0

    def parse_html(self):
        ''' 解释 html 文件
        获取代理ip
        '''
        if (os.path.exists(self.html_path)):
            for i in os.listdir(self.html_path):
                with open(self.html_path + i, 'r') as fp:
                    html = fp.read()

                soup = BeautifulSoup(html, 'lxml')

                tr_odd_res  = soup.find_all('tr', class_ = 'odd')
                tr_even_res = soup.find_all('tr', class_ = 'even')

                self.get_proxy_queue(tr_odd_res)
                self.get_proxy_queue(tr_even_res)

            self.size = self.proxy.qsize()
            print('HTML文件解释完成, 共获取Proxy: {}'.format(self.size))
        else:
            print('html目录不存在, 无法找到html文件进行解释.')

    def get_proxy_queue(self, tr_list):
        '''组装proxy队列
        解释tr获取td list, 从td中获取信息
        拼接proxy, 存进队列.
        '''
        for i in tr_list:
            td_res = i.find_all('td')

            protocol = 'http://' if td_res[-2].string == 'no' else 'https://'
            host     = td_res[0].string
            port     = td_res[1].string

            proxy = protocol + host + ':' + port
            self.proxy.put(proxy)

    def is_active(self, my_proxy):
        ''' proxy是否存活可用
        '''
        url      = 'https://www.zhipin.com/'
        protocol = my_proxy.split(':')[0]
        proxy    = {protocol: my_proxy}

        try:
            res = requests.get(url, proxies = proxy, timeout = 1)

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

    def save_proxy(self):
        '''把可用的proxy写进proxy.txt文件
        '''
        size = self.available_proxy.qsize()
        with open(self.proxy_file, 'w') as fp:
            while (not self.available_proxy.empty()):
                fp.write(self.available_proxy.get() + '\n')

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
        print('############ 获取代理ip ##############')
        self.parse_html()

        thread_num  = 10
        thread_list = []
        start_time  = time.time()

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
        print('\n')

        # 取消写入proxy.txt文件, 直接返回queue对象
        # self.save_proxy()
        return self.available_proxy
