# 更新中......

### 代理池服务器(Flask)

**代理池共分为四个模块：获取模块，存储模块，检测模块，api模块**

- 获取模块：主要通过元类实现，各大代理的抓取
- 存储模块：通过redis有序集合并通过检测模块检测代理是否可用
- 检测模块：通过asyncio和aiohttp实现异步并发请求，从而达到快读检测代理的有效性
- api模块：用flask构建一个本地api接口。每次访问本地接口，api都会从reids里调用可用的代理返回。对于实现高并发请求有点慢。所以直接从redis里获取可用代理会更快些

**成效**

- 在代理网站网页结构不更新的情况下代理池可以稳定的获取2000+以上的代理。对于检测不同的网站，代理的有效性数量也不一样。大部分网站都能够维持1000+以上的代理，对于小规模的数据采集任务已经够用了。

### Scrapy-redis 爬去新浪微博用户信息

**原理**

- spider解析下载器下载下来的response,返回item或者是links 
- item或者links经过spidermiddleware的process_spider_out()方法，交给engine。 
- engine将item交给itempipeline,将links交给调度器 
- 在调度器中，先将request对象利用scrapy内置的指纹函数，生成一个指纹对象 
- 如果request对象中的dont_filter参数设置为False,并且该request对象的指纹不在信息指纹的队列中，那么就把该request对象放到优先级的队列中 
- 从优先级队列中获取request对象，交给engine 
- engine将request对象交给下载器下载，期间会通过downloadmiddleware的process_request()方法 
- 下载器完成下载，获得response对象，将该对象交给engine,期间会通过downloadmiddleware的process_response()方法 
- engine将获得的response对象交给spider进行解析，期间会经过spidermiddleware的process_spider_input()方法 
- 从第一步开始循环

**模块**

- scrapy
- scrapy-redis
- redis
- mongodb：收集来的数据存放到mongodb中
- python的mongodb模块 
- python的redis模块

**部署**

使用Scrapyd服务

配置文件scrapyd.conf文件

[scrapyd]

...

[services]

...

**云部署**

docker容器，制作dockerfile文件

dockerfile:

- FROM python:3.6
- ADD . /code
- WORKDIR /code
- COPY ./scrapyd.conf /etc/scrapyd/
- EXPOSE 6800
- RUN pip3 install -r requirements.txt
- CMD scrapyd

构建镜像：

- docker build -t scrapyd:latest .

运行：

- docker run -d -p 6800:6800 scrapyd

#### Scrapy + Selenium爬取网易云音乐

准备：代理池，网易云会对访问频繁的操作做限制

运行：scrapy crawl music 

注意：获取到的评论很多都是重复的，需要进行去重操作

