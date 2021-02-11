# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from fake_useragent import UserAgent
import random
import time
import re
from tools.seleniumTest import platformJudge
from selenium import webdriver
import os
from selenium.webdriver.support.ui import  WebDriverWait

class RecruitspiderSpiderMiddleware(object):
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

class RandomUserAgentMiddleware(object):
    def __init__(self,crawler):
        super(RandomUserAgentMiddleware,self).__init__()

        self.ua = UserAgent(use_cache_server=True)
        self.ua_type = crawler.settings.get('USER_AGENT_TYPE','random')

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):

        def get_ua():
            return getattr(self.ua,self.ua_type)

        request.headers.setdefault('User-Agent',get_ua())

# class MyProxiesSpiderMiddleware(object):
#     def process_request(self, request, spider):
#         key = random.randint(1,2)
#         if key:
#             request.meta["proxy"] = "http://47.52.89.72:3128"

class JsPageMiddleware(object):
    def __init__(self):
        super(JsPageMiddleware,self).__init__()
        # 谷歌浏览器
        # chrome_opt = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_sttings.images": 2}
        # chrome_opt.add_experimental_option("prefs", prefs)
        # driver_path = platformJudge()
        # self.browser = webdriver.Chrome(driver_path, chrome_options=chrome_opt)

    def process_request(self, request, spider):
        regx = re.compile(r'\d+.html')
        res = re.findall(regx, request.url)
        # self.browser.set_page_load_timeout(20)
        # self.browser.set_script_timeout(20)
        if spider.name == 'lagou' and res and request.meta.get('curNum') != 1:
            # 拉钩处理
            spider.browser.get(request.url)
            # 找到元素就停止加载，否则刷新
            try:
                WebDriverWait(driver=spider.browser, timeout=5).until(lambda x: x.find_element_by_id('container'))
            except Exception as e:
                spider.browser.refresh()
            # 不经过downloader 直接返回结果
            return HtmlResponse(url=spider.browser.current_url,body=spider.browser.page_source,encoding="utf-8")
        elif spider.name == 'zhilian':
            # 智联招聘处理 只抓列表页
            url = request.url
            res = re.match(r'http://.*?/(.*?).htm', url)
            if not res:
                spider.browser.get(request.url)
                # 找到元素就停止加载，否则刷新
                try:
                    WebDriverWait(driver=spider.browser, timeout=5).until(lambda x: x.find_element_by_xpath("//div[contains(@class,'details_container')]"))
                except Exception as e:
                    spider.browser.refresh()
                # 不经过downloader 直接返回结果
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")
        elif spider.name == 'boss':
            # boss 直聘招聘处理
            url = request.url
            res = re.match(r'https://www.zhipin.com/job_detail/?query=&scity=(.*?)&industry=&position=', url)
            if not res:
                spider.browser.get(request.url)
                # 找到元素就停止加载，否则刷新
                try:
                    WebDriverWait(driver=spider.browser, timeout=5).until(
                        lambda x: x.find_element_by_id("//div[contains(@class,'main')]"))
                except Exception as e:
                    spider.browser.refresh()
                # 不经过downloader 直接返回结果
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")
