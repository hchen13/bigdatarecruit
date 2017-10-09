# -*- coding: utf-8 -*-
import scrapy
from tools.getFilterName import getCityPinYin
from urllib import parse as ps
from scrapy import Request

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['jobs.zhaopin.com/']
    start_urls = ['http://jobs.zhaopin.com/']
    # custom_settings = {
    # }

    headers = {
        'Referer': 'http://jobs.zhaopin.com/',
        'Origin': 'http://jobs.zhaopin.com/',
    }

    def start_requests(self):
        # 组建爬取城市链接
        for item in getCityPinYin():
            yield Request(ps.urljoin('http://jobs.zhaopin.com', item), headers=self.headers)

    def parse(self, response):
        print(response.url)

