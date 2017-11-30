import random
import sys

import requests
from bs4 import BeautifulSoup

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

    def __init__(self, key_word):
        '''
        @param  搜索职位关键字, 例如: php, python...
        @param  城市区域
        @param  命令行写入文本的长度(单行)
        '''
        self.key_word   = key_word
        self.area       = {}
        self.status_len = 0

    def write_cli(self, msg):
        ''' 命令行输出文本, 不换行
        '''
        sys.stdout.write('\r'*self.status_len)
        sys.stdout.write(msg)
        sys.stdout.flush()
        self.status_len = len(msg)

    def get_area(self):
        ''' 获取某城市的区域
        '''
        print('############## 区域爬取 ##############')

        url = 'https://www.zhipin.com/job_detail/?query=' + self.key_word + '&scity=' + str(Spider.city) + '&source=2';
        header = {
            'User-Agent': Spider.browsers[random.randint(0, len(Spider.browsers) - 1)]
        }
        html = requests.get(url, headers = header).content.decode('utf-8')

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

        for area, l in self.area.items():
            msg = ''
            self.status_len = 0

            msg += area + ': '
            self.write_cli(msg)

            url    = "https://www.zhipin.com/c" + str(Spider.city) + "/b_" + area + "-h_" + str(Spider.city) + "/?query="+self.key_word+"&ka=" + l[0]
            header = {
                'User-Agent': Spider.browsers[random.randint(0, len(Spider.browsers) - 1)]
            }
            html   = requests.get(url, headers = header).content.decode('utf-8')

            soup = BeautifulSoup(html, 'lxml')
            dl_res = soup.find_all('dl', class_ = 'condition-area show-condition-area')

            data = []
            for tag in dl_res[0].find_all('a'):
                if (tag.string != '不限'):
                    ka       = tag.attrs['ka']
                    business = tag.string
                    data.append([business, ka])
                    self.area[area] = data

                    msg += business + ' '
                    self.write_cli(msg)

            sys.stdout.write('\n')

        self.status_len = 0
        print('\n')

    def get_position(self):
        ''' 爬取职位信息
        '''
        print('############## 职位信息爬取 ##############')

    def run(self):
        self.get_area()
        self.get_business()
        self.get_position()


if __name__ == '__main__':
    spider = Spider('php')
    spider.run()
