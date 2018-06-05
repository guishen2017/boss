# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import json
import requests
from boss.models import ProxyModel
from twisted.internet.defer import DeferredLock

class UserAgentProxy(object):
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self,request, spider):
        user_agent = self.ua.random
        print(user_agent)
        request.headers.setdefault("User-Agent", user_agent)

class IPProxy(object):

    PROXY_URL = "http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=1&pack=21267&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="

    def __init__(self):

        self.lock = DeferredLock()
        self.current_proxy = None

    def process_request(self, request, spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            self.update_proxy()
        request.meta['proxy'] = self.current_proxy.proxy

    def process_response(self, request, response, spider):
        if response.status != 200:
            if not self.current_proxy.is_block:
                self.current_proxy.is_block = True
            self.update_proxy()
            return request
        return response

    def update_proxy(self):
        self.lock.acquire()
        if self.current_proxy is None or self.current_proxy.is_expiring or self.current_proxy.is_block:
            response_json = requests.get(self.PROXY_URL).json()
            try:
                print(response_json)
                self.current_proxy = ProxyModel(response_json['data'][0])
            except:
                print('出错了！')
                print(response_json)
        self.lock.release()


