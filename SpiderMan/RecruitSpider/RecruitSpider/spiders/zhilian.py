# -*- coding: utf-8 -*-
import scrapy
from tools.getFilterName import getCityPinYin
from urllib import parse as ps
from scrapy import Request
from urllib import parse

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
        # 获取职位列表
        position_list = response.xpath("//div[contains(@class,'details_container')]")

        # 判断如果有职位信息
        if len(position_list) > 0:
            for position_node in position_list:
                # 职位详情页
                position_url = position_node.xpath("span[contains(@class,'post')]/a/@href").extract_first()
                yield Request(url=parse.urljoin(response.url, position_url), headers=self.headers, callback=self.position_detail)
                # 公司工商信息详情页
                company_url = position_node.xpath("span[contains(@class,'company_name')]/a/@href").extract_first()
                if 'special' not in company_url:
                    yield Request(url=parse.urljoin(response.url, company_url), headers=self.headers, callback=self.company_detail)
        # 获取下一页
        next_url = response.xpath("//div[@class='searchlist_page']/span[@class='search_page_next']/a/@href").extract_first()
        yield Request(url=parse.urljoin(response.url, next_url), headers=self.headers, callback=self.parse)

    # 职位信息
    def position_detail(self, response):
        pass

    # 公司信息
    def company_detail(self, response):
        pass