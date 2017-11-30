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

        @ToDo
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
        print('############## 区域爬取 ##############')

        url = 'https://www.zhipin.com/job_detail/?query={key_word}&scity={city}&source=2'.format(key_word = self.key_word, city = Spider.city);
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

        url_template = "https://www.zhipin.com/c{city}/b_{area}-h_{city}/?query={key_word}&ka={ka}"
        for area, l in self.area.items():
            msg = ''
            self.status_len = 0

            msg = msg + area + ': '
            self.write_cli(msg)

            url    = url_template.format(city = Spider.city, area = area, key_word = self.key_word, ka = l[0])
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

                    msg = msg + business + ' '
                    self.write_cli(msg)

            sys.stdout.write('\n')

        self.status_len = 0
        print('\n')

    def get_position(self):
        ''' 爬取职位信息
        '''
        print('############## 职位信息爬取 ##############')

        url_template = "https://www.zhipin.com/c{city}/a_{business}-b_{area}-h_{city}/?query={key_word}&page={page}&ka=page-{page}"
        for area, business in self.area.items():
            for i in business:
                # 经测试, 20页数据就没了, 这里给100, 若发现没有找到 job list, 则中止, break
                for page in range(1, 100):
                    url = url_template.format(area = area, business = i[0], city = Spider.city, key_word = self.key_word, page = page)
                    header = {
                        'User-Agent': Spider.browsers[random.randint(0, len(Spider.browsers) - 1)]
                    }
                    html = requests.get(url, headers = header).content.decode('utf-8')
                    soup = BeautifulSoup(html, 'lxml')


    def run(self):
        self.get_area()
        self.get_business()
        self.get_position()


if __name__ == '__main__':
    spider = Spider('php')
    spider.run()
