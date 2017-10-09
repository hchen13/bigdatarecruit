# -*- coding: utf-8 -*-
import scrapy
from tools.getFilterName import getCityPinYin

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'

    # custom_settings = {
    # }

    allowed_domains = ['jobs.zhaopin.com/']
    start_urls = ['http://jobs.zhaopin.com//']

    def parse(self, response):
        pass
