# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from RecruitSpider.items import Job51ItemLoader, Job51CompanyItem, Job51PositionItem

class Job51(scrapy.spider):
    name = 'job51'
    allowed_domains = ['51job.com']
    start_urls = ['http://search.51job.com/']

    def parse(self, response):
        city_obj_arr =  response.css(".pcon span").extract()
        for node in city_obj_arr:
            city_url = node.css("a::attr(href)").extract_first()
            city_name = node.css("a::text").extract_first()
            yield Request(url=city_url, meta={'city_name': city_name}, callback=self.findCityPositionList)


    # 获取城市代码
    def findCityPositionList(self, response):
        p = re.compile(r'http://search.51job.com/list/(\d+),\"')
        city_code = p.findall(response.text)[2]
        position_list_url = "http://search.51job.com/list/" + city_code + ",000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        yield Request(url=position_list_url, meta={'city_code': city_code, 'city_name': response.meta.get('city_name')}, callback=self.positionList)

    # 职位列表页
    def positionList(self, response):
        position_arr = response.css(".dw_table div[class='el']")
        for item in position_arr:
            position_name = item.xpath("p/span/a/@title").extract_first()
            position_url = item.xpath("p/span/a/@href").extract_first()
            company_name = item.xpath("span[@class='t2']/a/@title").extract_first()
            company_url = item.xpath("span[@class='t2']/a/@href").extract_first()
            district = item.xpath("span[@class='t3']/text()").extract_first()
            salary = item.xpath("span[@class='t4']/text()").extract_first()
            publish_time = item.xpath("span[@class='t5']/text()").extract_first()
            param_diliver = {
                'city_code': response.meta.get('city_code'),
                'city_name': response.meta.get('city_name'),
                'position_name': position_name,
                'company_name': company_name,
                'district': district,
                'salary': salary,
                'publish_time': publish_time
            }
            yield Request(url=position_url, meta=param_diliver, callback=self.positionDetail)
            yield Request(url=company_url, meta=param_diliver, callback=self.companyDetail)

    def positionDetail(self, response):
        city_name = response.meta.get('city_name')
        if len(response.css("sp4")) == 4:
            education = response.css('.sp4:nth-child(2)').extract_first()
            recruit_num = response.css('.sp4:nth-child(3)').extract_first()
        else:
            education = "NULL"
            recruit_num = re.sub('招', '', str(response.css('.sp4:nth-child(2)').extract_first()))

        label_second = response.css(".sp2::attr(title)").extract()
        language = label_second[0] if label_second and label_second[0] else 'NULL'
        labels_1 = label_second[0] if label_second and label_second[1] else ''
        company_label = re.sub(r"\s+", '', response.css(".cn p:last-child::text").extract_first()).split('|')[2]
        position_labels = company_label + ' ' + labels_1
        position_labels = position_labels.split(' ')

        item_loader = Job51ItemLoader(item=Job51PositionItem(), response=response)
        item_loader.add_value('city_code', response.meta.get('city_code'))
        item_loader.add_value('city_name', city_name)

        item_loader.add_value('name', response.meta.get('position_name'))

        item_loader.add_value('district', re.sub(city_name + '-', '', str(response.meta.get('district'))))
        item_loader.add_value('salary', response.meta.get('salary'))
        item_loader.add_value('company_md5', response.meta.get('company_name'))
        item_loader.add_css('work_year', '.sp4:nth-child(1)::text')
        item_loader.add_value('education', education)
        item_loader.add_value('recruit_num', recruit_num)
        item_loader.add_value('publish_time', response.meta.get('publish_time'))
        item_loader.add_value('language', language)


    def companyDetail(self, response):
        pass
