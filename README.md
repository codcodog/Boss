Boss 爬虫
=========

### 如何使用
```
$ git clone https://github.com/codcodog/Boss.git
$ cd Boss

Boss $ pyvenv venv # 或者 virtualenv venv
Boss $ source venv/bin/active

(venv) Boss $ pip install -r requirements.txt 
(venv) Boss $ python boss.py
```
笔者的运行环境: `Arch Linux/Centos6.5` + `Python 3.6.3`  
数据使用 `sqlite3` 存储在 `boss.db`.  
职位信息: `区域`, `商圈`, `薪资`, `工作年限`, `行业类型`

### 遇到的困难
Boss 反爬虫机制: 封禁IP (403)

场景描述:  
运行爬虫, 多线程爬取的时候，当爬取到一定量的时候, 提示输入验证码, 更换 Proxy IP 继续爬取, 还是提示输入验证码, 一直循环这个过程, 最后 IP 被封.  
这里的 IP 是指真实 IP, 也就是说, 使用的代理 IP 没有起到它应有的作用.  
有点好奇反爬虫的逻辑是如何实现的, 又是怎样识别到我的真实 IP, 毕竟我使用的是高匿代理.  
(PS: 什么是高匿代理, 看下面介绍.)

### 解决的办法
- 设置爬取速度尽可能慢
- 多线程爬取修改为单线程爬取
- ~~当要求输入验证码的时候, 爬虫程序睡眠一下, 然后手动在浏览器输入验证码.~~  

PS: 有条件的，可以把爬虫放置到个人服务器上， 使用`守护进程`进行爬取，避免个人PC等待时间过长.
```
$ nohup python -u boss.py > crawl.log &
```
> 使用 `-u` 选项是为了避免 `python` 标准输出缓冲.  

具体了解，可以参考: [nohup python 脚本，重定向输出，日志内容为空](https://github.com/codcodog/Blog/issues/76)

### 代理
#### 透明代理 (Transparent Proxy)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Proxy IP
- HTTP_X_FORWARDED_FOR = Your IP

> 透明代理虽然可以直接“隐藏”你的IP地址，但是还是可以从HTTP_X_FORWARDED_FOR来查到你是谁.

#### 匿名代理 (Anonymous Proxy)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Proxy IP
- HTTP_X_FORWARDED_FOR = Proxy IP

> 匿名代理比透明代理进步了一点: 别人只能知道你用了代理, 但无法知道是谁(真实IP).

#### 混淆代理 (Distorting Proxies)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Proxy IP
- HTTP_X_FORWARDED_FOR = Random IP Address

> 与匿名代理一样, 如果使用了混淆代理, 别人还是能知道你使用了代理, 但是会得到一个假的IP地址, 伪装的更加逼真.

#### 高匿代理 (Elite Proxy / High Anonymity Proxy)
- REMOTE_ADDR = Proxy IP
- HTTP_VIA = Not determined
- HTTP_X_FORWARDED_FOR = Not determined

> 可以看到, 高匿代理让别人无法发现你是在用代理.

### 图表数据
[图表分析](http://65.49.200.193/boss/analysis.php)
