# -*- coding: utf-8 -*-
import scrapy
from tools.getFilterName import getCityPinYin
from RecruitSpider.items import ZhilianItemLoader, ZhilianItem
from urllib import parse as ps
from scrapy.http import Request
import re

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://jobs.zhaopin.com/']

    headers = {
        'Referer': 'http://jobs.zhaopin.com/beijing/',
        'Origin': 'http://jobs.zhaopin.com/',
        'Cache_Control': "max-age=0",
        'Connection': 'keep-alive',

    }

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'RecruitSpider.pipelines.ZhilianSpiderPipeline': 300,
        },
    }

    def start_requests(self):
        # 组建爬取城市链接
        for item in getCityPinYin():
            print(item)
            yield Request(ps.urljoin('http://jobs.zhaopin.com', item), headers=self.headers, meta={'page_num':1})

    def parse(self, response):
        # 获取职位列表
        position_list = response.xpath("//div[contains(@class,'details_container')]")

        page_obj = re.match(r"http://.*?/.*?/p(\d*)/$", response.url)
        page_num = page_obj[1] if page_obj else 1
        print(position_list[0].xpath("span[contains(@class,'address')]/text()").extract_first() + " 第" + str(page_num) + "页, 共" + str(len(position_list)))
        # 判断如果有职位信息
        if len(position_list) > 0:
            for position_node in position_list:
                # 职位详情页
                position_url = position_node.xpath("span[contains(@class,'post')]/a/@href").extract_first()
                # 公司工商信息详情页
                company_url = position_node.xpath("span[contains(@class,'company_name')]/a/@href").extract_first()

                yield Request(url=ps.urljoin(response.url, position_url), headers=self.headers, meta={'company_url': company_url}, callback=self.position_detail)
        # 获取下一页
        next_url = response.xpath("//div[@class='searchlist_page']/span[@class='search_page_next']/a/@href").extract_first()
        if next_url:
            yield Request(url=ps.urljoin(response.url, next_url), headers=self.headers, callback=self.parse, meta={'page_num': response.meta.get("page_num") + 1})

    # 职位信息
    def position_detail(self, response):
        item_loader = ZhilianItemLoader(item=ZhilianItem(), response=response)
        company_name = response.xpath("//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/h2/a/text()").extract_first()

        # 没有公司信息的职位不予录取
        if company_name:
            # 公司zhilian_company item
            item_loader.add_xpath('company_md5', "//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/h2/a/text()")
            item_loader.add_xpath('full_name', "//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/h2/a/text()")
            logo_url = response.xpath("//div[contains(@class,'company-box')]/p[contains(@class,'img-border')]/a/img/@src").extract_first()
            item_loader.add_value('logo', logo_url if logo_url else 'NULL')

            item_loader.add_xpath('size', "//div[contains(@class,'company-box')]/ul/li[1]/strong/text()")
            item_loader.add_xpath('company_nature', "//div[contains(@class,'company-box')]/ul/li[2]/strong/text()")

            if len(response.xpath("//div[contains(@class,'company-box')]/ul/li")) == 5:
                item_loader.add_xpath('industry', "//div[contains(@class,'company-box')]/ul/li[3]/strong/a/text()")
                item_loader.add_xpath('website', "//div[contains(@class,'company-box')]/ul/li[4]/strong/a/text()")
                # 需要二次处理字段，原因：去掉空白字符和换行符
                item_loader.add_xpath('address', "//div[contains(@class,'company-box')]/ul/li[5]/strong/text()")
            else:
                item_loader.add_value('website', "NULL")
                item_loader.add_xpath('industry', "//div[contains(@class,'company-box')]/ul/li[3]/strong/a/text()")
                # 需要二次处理字段，原因：去掉空白字符和换行符
                item_loader.add_xpath('address', "//div[contains(@class,'company-box')]/ul/li[4]/strong/text()")

            item_loader.add_value('company_url', response.meta.get("company_url"))

            # 智联招聘职位zhilian_position item
            item_loader.add_xpath('position_name', "//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/h1/text()")
            item_loader.add_xpath('salary_low', "//div[contains(@class,'terminalpage-left')]/ul/li[1]/strong/text()")
            item_loader.add_xpath('salary_high', "//div[contains(@class,'terminalpage-left')]/ul/li[1]/strong/text()")
            item_loader.add_xpath('city', "//div[contains(@class,'terminalpage-left')]/ul/li[2]/strong/a/text()")
            item_loader.add_xpath('publish_time', "//div[contains(@class,'terminalpage-left')]/ul/li[3]/strong/span/text()")
            item_loader.add_xpath('job_nature', "//div[contains(@class,'terminalpage-left')]/ul/li[4]/strong/text()")
            item_loader.add_xpath('work_year', "//div[contains(@class,'terminalpage-left')]/ul/li[5]/strong/text()")
            item_loader.add_xpath('education', "//div[contains(@class,'terminalpage-left')]/ul/li[6]/strong/text()")

            # 需要二次处理字段， 原因：去掉人数的人字
            item_loader.add_xpath('recruit_num', "//div[contains(@class,'terminalpage-left')]/ul/li[7]/strong/text()")
            item_loader.add_xpath('position_type', "//div[contains(@class,'terminalpage-left')]/ul/li[8]/strong/a/text()")
            # 需要二次处理字段。 原因：md5

            unique_md5 = response.xpath("//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/h1/text()").extract_first() + company_name + response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[3]/strong/span/text()").extract_first()
            item_loader.add_value('unique_md5', unique_md5)
            content_arr = response.xpath("//div[contains(@class,'terminalpage-main')]/div[contains(@class,'tab-cont-box')]/div[1]/p[position() < last()]").extract()
            if not content_arr:
                content_arr = response.xpath("//div[contains(@class,'terminalpage-main')]/div[contains(@class,'tab-cont-box')]/div[1]/div/p[position() < last()]").extract()
            item_loader.add_value('content', ''.join(content_arr))
            # 需要二次处理字段 原因：去掉空白字符和换行符
            item_loader.add_xpath('location', "//div[contains(@class,'terminalpage-main')]/div[contains(@class,'tab-cont-box')]/div[1]/h2/text()")
            item_loader.add_value('url', response.url)
            # 需要二次处理字段 原因：数组
            advantage_labels = ','.join(response.xpath("//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/div[contains(@class,'welfare-tab-box')]/span/text()").extract())
            item_loader.add_value('advantage_labels', advantage_labels if advantage_labels else "NULL")

            position_detail_item = item_loader.load_item()
            yield position_detail_item