# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class MyspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


import random
import base64
from .settings import  USER_AGENTS

class Random_txt_Proxy(object):
    def process_request(self, request, spider):
        with open('E:/python_code/Search/learn_scrapy/mySpider/proxy.txt','r') as f:
            proxies = f.readlines()
        proxy = random.choice(proxies)

        # if proxy['user_passwd'] is None:
            # 没有代理账户验证的代理使用方式
        request.meta['proxy'] = "https://" + proxy
        print(proxy)
        # else:
        #     # 对账户密码进行base64编码转换
        #     base64_userpasswd = base64.b64encode(proxy['user_passwd'])
        #     # 对应到代理服务器的信令格式里
        #     request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
        #     request.meta['proxy'] = "http://" + proxy['ip_port']


import requests
import json
class Random_api_Proxy(object):

    def __init__(self):
        self.url = 'http://svip.kdlapi.com/api/getproxy/?orderid=926946570785595&num=100&protocol=2&me' \
                   'thod=2&an_an=1&an_ha=1&quality=2&format=json&sep=1'
        self.flag = 1
        self.get_proxies_num = 1
        self.lists = requests.get(self.url).json()
        self.proxies = self.lists['data']['proxy_list']


    #
    def get_proxies(self):
        lists = requests.get(self.url).json()
        proxies = lists['data']['proxy_list']
        return proxies  #返回列表


    def process_request(self, request, spider):
        PROXIES = self.proxies
        if self.get_proxies_num == 1 or self.get_proxies_num == 32:
            PROXIES = self.get_proxies()

        if self.flag >32:
            proxy = random.choice(PROXIES)
            request.meta['proxy'] = "http://" + proxy
            self.flag = 1
            self.get_proxies_num += 1
            print(proxy)
        else:
            self.flag +=1







# 随机的User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):

        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)
