import random
import sys
import queue
import threading
import time
import datetime

import requests
from bs4 import BeautifulSoup
from crawl.db import Db

# 全局互斥锁
mutex = threading.Lock()

class Spider:
    '''
    @param  城市代号: 深圳
    @param  浏览器标识
    '''
    city       = 101280600
    browsers   = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) ",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ",
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    ]

    def __init__(self, key_word, proxy = None, db_file = None):
        '''
        @param  搜索职位关键字, 例如: php, python...
        @param  城市区域
        @param  命令行写入文本的长度(单行)
        @param  代理ip队列
        @param  当前请求的页数
        @param  sqlite3 数据库对象
        @param  写入数据库的队列: 职位信息
        '''
        self.key_word   = key_word
        self.area       = {}
        self.status_len = 0
        self.proxy      = proxy
        self.page       = 1
        self.db         = Db(db_file)
        self.position   = queue.Queue()

    def write_cli(self, msg):
        ''' 命令行输出文本, 不换行

        @bug
        遇到比较诡异的情况, 就是宽屏的时候, 一行没有超过屏幕, 按照正常输出:
        盐田区: 大梅沙 沙头角 
        宝安区: 西乡 新安 龙华 民治 福永 沙井 翻身路 石岩 观澜 锦绣江南 桃源居 坂田 松岗 
        福田区: 车公庙 上步 岗厦 皇岗 石厦 沙头 梅林 购物公园 八卦岭 华强北 竹子林 上梅林 益田村 景田 香蜜湖 蔡屋围 下沙 新洲 振华路 园岭 沙嘴 泥岗 
        龙华区: 龙华 民治 锦绣江南 观澜 滢水山庄 坂田 
        南山区: 科技园 大冲 南头 深圳湾 西丽 蛇口 前海 南油 后海 华侨城 海上世界 海王大厦 白石洲 桃源村 
        龙岗区: 坂田 平湖 横岗 布吉 滢水山庄 万科城 坪地 坪山 
        坪山区: 坪山 
        罗湖区: 东门 国贸 笋岗 莲塘 翠竹 火车站 布心 泥岗 田贝 蔡屋围 黄贝岭 布吉 文锦渡 东晓 水贝 清水河 

        但是, 如果是窄屏, 例如: 在我的竖屏, 会重复输出(也就是回退没有生效), 如下:
        罗湖区: 东门 国贸 笋岗 莲塘 翠竹 火车站 布心 泥岗 田贝 蔡屋围 黄贝岭 布吉 文锦渡 东晓 水贝 清水河 
        南山区: 科技园 大冲 南头 深圳湾 西丽 蛇口 前海 南油 后海 华侨城 海上世界 海王大厦 白石洲 桃源村 
        宝安区: 西乡 新安 龙华 民治 福永 沙井 翻身路 石岩 观澜 锦绣江南 桃源居 坂田 松岗 
        坪山区: 坪山 
        盐田区: 大梅沙 沙头角 
        龙华区: 龙华 民治 锦绣江南 观澜 滢水山庄 坂田 
        福田区: 车公庙 上步 岗厦 皇岗 石厦 沙头 梅林 购物公园 八卦岭 华强北 竹子林 上梅林 益田村 景田 香蜜湖 蔡屋围 下沙 新洲 福田区: 车公庙 上步 岗厦 皇岗 石厦 沙头 梅林 购物公园 八卦岭 华强北 竹子林 上梅林 益田村 景田 香蜜湖 蔡屋围 下沙 新洲 福田区: 车公庙 上步 岗厦 皇岗 石厦 沙头 梅林 购物公园 八卦岭 华强北 竹子林 上梅林 益田村 景田 香蜜湖 蔡屋围 下沙 新洲 福田区: 车公庙 上步 岗厦 皇岗 石厦 沙头 梅林 购物公园 八卦岭 华强北 竹子林 上梅林 益田村 景田 香蜜湖 蔡屋围 下沙 新洲 振华路 园岭 沙嘴 泥岗 
        龙岗区: 坂田 平湖 横岗 布吉 滢水山庄 万科城 坪地 坪山 
        '''
        sys.stdout.write('\r' * self.status_len)
        sys.stdout.write(msg)
        sys.stdout.flush()
        self.status_len = len(msg)

    def get_area(self):
        ''' 获取某城市的区域
        '''
        print('\n############## 区域爬取 ##############')

        url   = 'https://www.zhipin.com/job_detail/?query={key_word}&scity={city}&source=2'.format(key_word = self.key_word, city = Spider.city);
        proxy = self.get_proxy()

        while (True):
            header = {
                'User-Agent': Spider.browsers[random.randint(0, len(Spider.browsers) - 1)],
            }
            try:
                html = requests.get(url, headers = header, proxies = proxy, timeout = 5).content.decode('utf-8')
            except requests.exceptions.RequestException:
                print('请求失败, 更换代理, 重新请求, 剩余proxy: %s' % self.proxy.qsize())
                time.sleep(random.randint(3, 5))

                proxy = self.get_proxy()
                continue
            else:
                break

        soup   = BeautifulSoup(html, 'lxml')
        dl_res = soup.find_all('dl', class_  = 'condition-district show-condition-district')

        msg = ''
        for tag in dl_res[0].find_all('a'):
            if (tag.string != '不限'):
                ka        = tag.attrs['ka']
                area_name = tag.string

                self.area.setdefault(area_name, [ka])

                msg += area_name + ' '
                self.write_cli(msg)

        # 重置写入值的长度
        self.status_len = 0
        print('\n')


    def get_business(self):
        ''' 获取某区域的商圈
        '''
        print('############## 商圈爬取 ##############')

        url_template = "https://www.zhipin.com/c{city}/b_{area}-h_{city}/?query={key_word}&ka={ka}"
        proxy = self.get_proxy()
        for area, l in self.area.items():
            msg = ''
            self.status_len = 0

            msg = msg + area + ': '
            self.write_cli(msg)

            url    = url_template.format(city = Spider.city, area = area, key_word = self.key_word, ka = l[0])
            while True:
                header = {
                    'User-Agent': Spider.browsers[random.randint(0, len(Spider.browsers) - 1)],
                }
                try:
                    html   = requests.get(url, headers = header, proxies = proxy).content.decode('utf-8')
                except requests.exceptions.RequestException:
                    print('请求失败, 更换代理, 重新请求, 剩余proxy: %s' % self.proxy.qsize())
                    time.sleep(3)

                    proxy = self.get_proxy()
                    continue
                else:
                    break

            soup = BeautifulSoup(html, 'lxml')
            dl_res = soup.find_all('dl', class_ = 'condition-area show-condition-area')

            data = []
            for tag in dl_res[0].find_all('a'):
                if (tag.string != '不限'):
                    self.area[area].append(tag.string)

                    msg = msg + tag.string + ' '
                    self.write_cli(msg)

            sys.stdout.write('\n')
            time.sleep(random.randint(5, 10))

        self.status_len = 0

    def get_position(self):
        ''' 爬取职位
        '''
        print('\n############## 职位爬取 ##############')

        url_template = "https://www.zhipin.com/c{city}/a_{business}-b_{area}-h_{city}/?query={key_word}"
        for area, business in self.area.items():
            # 删除第一个无关元素
            del business[0]

            for b in business:
                # 经测试, 20页数据就没了, 这里给100, 若发现没有找到 job list, 则中止, break
                url = url_template.format(area = area, business = b, city = Spider.city, key_word = self.key_word)
                self.page = 1
                self.concurrent_crawl(url, area, b)

                print('>>> %s %s 爬取完成 <<<\n' % (area, b))

                # 把职位信息存储进数据库
                self.position_to_db()
                time.sleep(random.randint(3, 5))

                # 判断一下proxy, 如果用完, 则终止程序
                if (not self.proxy.qsize()):
                    print('Proxy用完, 退出程序.')
                    raise SystemExit
            else:
                print('爬取完成.')


    def concurrent_crawl(self, url, area, business):
        ''' 多线程爬取
        '''
        thread_num  = 1
        thread_list = []

        for i in range(thread_num):
            t = threading.Thread(target = self.crawl_position, args = (url, area, business))
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()


    def crawl_position(self, url, area, business):
        ''' 爬取职位信息
        '''
        proxy = self.get_proxy()
        url_template = url + "&page={page}&ka=page-{page}"

        while (True):
            url = url_template.format(page = self.page)

            # 修改线程共享变量
            if (mutex.acquire()):
                self.page += 1
                mutex.release()

            while (True):
                header = {
                    'User-Agent': Spider.browsers[random.randint(0, len(Spider.browsers) - 1)],
                }

                # connetion error 则换proxy, proxy失效
                try:
                    print('爬取: %s %s %s页' % (area, business, self.page - 1))
                    html = requests.get(url, headers = header, proxies = proxy, timeout = 5).content.decode('utf-8')
                except requests.exceptions.RequestException:
                    msg = 'proxy失效, 更换proxy, 5s后重新爬取, 剩余proxy: %s' % self.proxy.qsize()
                    print(msg)

                    proxy = self.get_proxy()
                    time.sleep(5)
                    continue

                soup     = BeautifulSoup(html, 'lxml')
                job_list = soup.find_all('div', class_ = 'job-list')

                # 如果没有job_list, 说明请求过多需要输入验证码, 更换proxy重新请求
                if (not job_list):
                    print('请求过多, 要求输入验证码, 更换proxy重新爬取, 剩余proxy: %s' % self.proxy.qsize())
                    proxy = self.get_proxy()
                    time.sleep(random.randint(20, 30))
                    continue
                # 有数据则退出循环
                else:
                    break

            job_li = job_list[0].find_all('li')

            # 如果没有job_li, 说明没有数据了, 没有下一页, 退出循环
            if (not job_li):
                break

            self.parse_position(job_li, area, business)

            # 爬取完此页, 睡眠30~60s
            time.sleep(random.randint(45, 75))

    def parse_position(self, li_list, area, business):
        ''' 解释职位html, 并把职位信息写入sqlite3 数据库
        包括:
        工资, 年限, 行业类别, 职位发布时间
        '''
        for item in li_list:
            # 薪资
            span_res = item.find_all('span', class_ = 'red')
            salary   = span_res[0].string

            # 工作年限
            p_res = item.find_all('div', class_ = 'info-primary')[0].find_all('p')[0]
            p_res = str(p_res)
            tag   = '''<em class="vline"></em>'''
            age   = p_res.split(tag)[1]

            # 行业类型
            p1_res       = item.find_all('div', class_ = 'company-text')[0].find_all('p')[0]
            p1_res       = str(p1_res)
            tmp_list     = p1_res.split(tag)
            company_type = tmp_list[0].replace('<p>', '')

            # 职位发布时间
            # span_res = item.find_all('div', class_ = 'job-time')[0].find_all('span', class_ = 'time')[0]
            # job_time = span_res.string.replace('发布于', '')

            # if job_time == '昨天':
            #     today      = datetime.date.today()
            #     yeasterday = today - datetime.timedelta(days = 1)
            #     date       = yeasterday
            # else:
            #     date = time.strftime('%Y') + '-' + job_time.replace('月', '-').replace('日', '')
            # self.position.put((area, business, salary, age, company_type, date))
            self.position.put((area, business, salary, age, company_type))

    def position_to_db(self):
        ''' 将数据写进数据库
        '''
        while (not self.position.empty()):
            area, business, salary, age, company_type, date = self.position.get()
            self.db.insert_info(area, business, salary, age, company_type, date)

    def get_proxy(self):
        ''' 获取proxy
        '''
        # 用完proxy, 则退出程序, 不再向下执行
        if (self.proxy.empty()):
            print('Proxy 已经用完, 线程 %s 结束.' % threading.currentThread().getName())
            raise SystemExit
        else:
            my_proxy1      = self.proxy.get()
            protocol1      = my_proxy1.split(':')[0]
            proxy          = {
                protocol1: my_proxy1
            }

            return proxy

    def run(self):
        self.get_area()
        self.get_business()
        self.get_position()
