Boss 爬虫
=========

### 如何使用
```
$ git clone https://github.com/codcodog/Boss.git
$ cd Boss

Boss $ pyvenv venv
Boss $ source venv/bin/active

(venv) Boss $ pip install -r requirements.txt 
(venv) Boss $ python boss.py
```
运行环境: `Arch Linux` + `Python 3.5.2`  
爬取的数据存储在 `boss.db`, 使用 `sqlite3` 数据库.  
另外, 只爬取职位信息的: `区域`, `商圈`, `薪资`, `工作年限`, `行业类型`, `职位发布时间`.

### 遇到的困难
Boss 反爬虫机制: 封禁IP (403)

场景描述:  
一开始, 使用国外一个[站点](https://free-proxy-list.net/)的免费代理IP, 但是发现没有效果, 当爬取一定数目的时候, IP被封(本地IP), 从而导致爬取失败.  
也就是说, 代理IP没有起到效果, Boss 反爬虫可以识别到真实IP, IP 被封之后, 导致本地也没法访问 Boss.  
估计那个站点提供的是普通代理(透明代理), 可以追踪到本地IP, 但站点说提供的是高匿代理.  

于是, 换了一个国内[站点](http://www.kuaidaili.com/free/)提供的高匿代理, 但是还是遇到了一样的情况, 爬取一定的数目的时候, IP 被封, 本地IP 也受影响.  
真不知道它反爬虫的逻辑是如何实现的.

### 解决的办法
- 还是使用国内爬取的那个高匿代理
- 设置爬取速度尽可能慢
- 当遇到需要输入验证码的时候, 手动在浏览器输入 (一点都不程序员)

### 不同种类的代理
1. 透明代理 (Transparent Proxy)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Proxy IP
- HTTP_X_FORWARDED_FOR = Your IP

> 透明代理虽然可以直接“隐藏”你的IP地址，但是还是可以从HTTP_X_FORWARDED_FOR来查到你是谁.

2. 匿名代理 (Anonymous Proxy)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Proxy IP
- HTTP_X_FORWARDED_FOR = Proxy IP

> 匿名代理比透明代理进步了一点: 别人只能知道你用了代理, 但无法知道是谁(真实IP).

3. 混淆代理 (Distorting Proxies)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Proxy IP
- HTTP_X_FORWARDED_FOR = Random IP Address

> 与匿名代理一样, 如果使用了混淆代理, 别人还是能知道你使用了代理, 但是会得到一个假的IP地址, 伪装的更加逼真.

4. 高匿代理 (Elite Proxy / High Anonymity Proxy)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Not determined
- HTTP_X_FORWARDED_FOR = Not determined

> 可以看到, 高匿代理让别人根本无法发现你是在用代理.
