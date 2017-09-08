# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy import FormRequest
from SpiderMan.RecruitSpider.RecruitSpider.items import LagouItem,LagouItemLoader
class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/allCity.html?px=new&city=%E5%8C%97%E4%BA%AC']

    headers = {
        "HOST": "www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_?&px=new&city=%E5%8C%97%E4%BA%AC",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    }

    # 进入城市列表
    def parse(self, response):
        city_parent = response.xpath("//table[contains(@class,'word_list')]/tr")

        for city_node in city_parent:
            city_initial = city_parent.xpath("td[1]/div/span/text()").extract_first()
            city_initial_part = city_parent.xpath("td[2]/ul/li")
            for city_part in city_initial_part :
                city_name = city_part.xpath('a/text()').extract_first()
                url = city_part.xpath('input/@value').extract_first()
                yield Request(url=parse.urljoin(response.url,url), meta={'city_name':city_name,'city_initial':city_initial,'curNum':1}, callback=self.positionList)

    # 进入职位列表页
    def positionList(self,response):

        # 调拉钩自己的接口
        import requests
        import json
        # 组装接口链接
        city_str = {"city":response.meta.get('city_name')}
        url_city_str = parse.urlencode(city_str)
        url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&' + url_city_str + '&needAddtionalResult=false&isSchoolJob=0'
        # 获取当前页的页码
        # curNum = response.xpath('//span[contains(@class,"curNum")]/text()').extract_first()
        curNum = response.meta.get("curNum",1)
        query_data = {'first':False,'pn':curNum,'kd':''}
        res = requests.post(url=url, headers=self.headers, data=query_data).json()

        hrInfoMap = res['content']['hrInfoMap']
        positionResult = res['content']['positionResult']['result']
        totalNum = res['content']['positionResult']['totalCount']
        for item in positionResult:
            url = parse.urljoin("https://www.lagou.com/jobs", str(item["positionId"]) + '.html')
            yield Request(url=url, meta={"hrInfoMap": hrInfoMap}, callback=self.positionDetail)

        # 获取下一页
        yield Request()

    # 职位详情页
    def positionDetail(self,response):

        item_loader = LagouItemLoader(item=LagouItem,response=response)



        lagou_item = item_loader.load_item()
        yield lagou_item