# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request


class LagoucrawlerSpider(CrawlSpider):
    name = 'lagouCrawler'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin']

    rules = (
        Rule(LinkExtractor(allow=('www.lagou.com/jobs/',)), callback='parse_job'),
    )

    # def start_requests(self):
    #     return [Request('https://www.lagou.com/zhaopin/', headers=self.headers,callback=self.parse_next)]
    #
    # def parse_next(self,response):
    #     for i, url in enumerate(self.start_urls):
    #         yield self.make_requests_from_url(url)

    def parse_job(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
