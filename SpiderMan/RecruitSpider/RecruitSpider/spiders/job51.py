# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from RecruitSpider.items import Job51ItemLoader, Job51CompanyItem, Job51PositionItem


class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['jobs.51job.com', 'www.51job.com', 'search.51job.com']
    start_urls = ['http://search.51job.com/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'RecruitSpider.pipelines.Job51SpiderPipeline': 300,
        },
    }

    # headers = {
    #     'Host': 'http://www.51job.com/',
    #     'Referer': 'http://www.51job.com/',
    #     'Origin': 'http://www.51job.com/',
    #     'Connection': 'keep-alive',
    #     'Upgrade-Insecure-Requests': 1,
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
    # }

    city_total_num = 0
    city_num = 0
    def parse(self, response):
        city_obj_arr = response.css(".pcon span")
        self.city_total_num = len(city_obj_arr)
        for node in city_obj_arr:
            self.city_num += 1
            city_url = node.css("a::attr(href)").extract_first()
            city_name = node.css("a::text").extract_first()
            yield Request(url=city_url, meta={'city_name': city_name}, callback=self.findCityPositionList)

    # 获取城市代码
    def findCityPositionList(self, response):
        print(str(self.city_num) + '/' + str(self.city_total_num))
        p = re.compile(r'http://search.51job.com/list/(\d+),.*\"')
        city_code = p.findall(response.text)[2]
        position_list_url = "http://search.51job.com/list/" + city_code + ",000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        yield Request(url=position_list_url, meta={'city_code': city_code, 'city_name': response.meta.get('city_name'), 'n': 0 }, callback=self.positionList)

    # 职位列表页
    def positionList(self, response):
        n = response.meta.get('n') + 1
        print(response.meta.get('city_name') + ' 第' + str(n) + '页')
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

        # 下一页
        next_url = response.css('.dw_table .dw_page li.bk:last-child a::attr(href)').extract_first()
        if next_url:
            yield Request(url=next_url, meta={'city_name': response.meta.get('city_name'), 'city_code': response.meta.get('city_code'), 'n':n}, callback=self.positionList)

    def positionDetail(self, response):
        city_name = response.meta.get('city_name')
        if len(response.css(".sp4")) == 4:
            education = response.css('.sp4:nth-child(2)::text').extract_first()
            recruit_num = re.sub('招|人', '', response.css('.sp4:nth-child(3)::text').extract_first())
        else:
            education = "NULL"
            recruit_num = re.sub('招|人', '', str(response.css('.sp4:nth-child(2)::text').extract_first()))

        label_second = response.css(".sp2::attr(title)").extract()
        language = label_second[0] if label_second and len(label_second) != 1 else 'NULL'

        company_label = re.sub(r"\s+", '', str(response.css(".cn p:last-child::text").extract_first())).split('|')
        company_label = company_label[2] if len(company_label) > 2 else company_label[1]
        labels_1 = label_second[1] if label_second and len(label_second) > 1 else ''
        position_labels = company_label + ',' + labels_1
        position_labels = position_labels.split(',')

        item_loader = Job51ItemLoader(item=Job51PositionItem(), response=response)
        item_loader.add_value('city_code', response.meta.get('city_code'))
        item_loader.add_value('city_name', city_name)

        item_loader.add_value('name', response.meta.get('position_name'))

        item_loader.add_value('district', re.sub(city_name + '-', '', str(response.meta.get('district'))))
        salary = response.meta.get('salary')
        item_loader.add_value('salary', salary if salary else 'NULL')
        item_loader.add_value('company_md5', response.meta.get('company_name'))
        item_loader.add_css('work_year', '.sp4:nth-child(1)::text')
        item_loader.add_value('education', education)
        item_loader.add_value('recruit_num', recruit_num)
        item_loader.add_value('publish_time', response.meta.get('publish_time'))
        item_loader.add_value('language', language)
        item_loader.add_value('industry', position_labels)
        # 数组需要二次处理
        item_loader.add_css('position_labels', '.el::text')
        # 数组需要二次处理
        advantage = response.css(".jtag.inbox .t2 span::text").extract()
        item_loader.add_value('advantage', advantage if advantage else 'NULL')
        item_loader.add_value('content', response.css(".tBorderTop_box:nth-child(2)").extract_first().replace(
            response.css(".share").extract_first(), ''))
        location = re.sub('\t', '', str(response.css(".tBorderTop_box:nth-child(3) p::text").extract()))
        item_loader.add_value('location', location[1] if location else 'NULL')

        # 获取电话和email
        email_regex = re.compile(r"[a-zA-Z0-9]+[\_]*[a-zA-Z0-9]+[@|#][a-zA-Z0-9]+\.[a-zA-Z0-9]+[[\.]*[a-zA-Z0-9]*]*")
        phone_regex = re.compile(r"[\d]{3,8}-[\d]{4,11}[-\d+]*")
        telephone_regex = re.compile(r"[\d]{11}")
        email = list(set(email_regex.findall(','.join(response.css(".tBorderTop_box").extract()))))
        phone_num = list(set(
            phone_regex.findall(','.join(response.css(".tBorderTop_box").extract())) + telephone_regex.findall(
                ','.join(response.css(".tBorderTop_box").extract()))))

        item_loader.add_value('email', email if email else 'NULL')
        item_loader.add_value('phone_num', phone_num if phone_num else 'NULL')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_md5', response.url)
        job51_item = item_loader.load_item()
        yield job51_item

    def companyDetail(self, response):
        item_loader = Job51ItemLoader(item=Job51CompanyItem(), response=response)
        item_loader.add_value('company_md5', response.meta.get('company_name'))
        item_loader.add_value('full_name', response.meta.get('company_name'))
        labels_part = re.sub(r'\s+', '', str(response.css(".tHeader.tHCop .in p::text").extract_first())).split('|')
        size = labels_part[1] if len(labels_part) > 2 else 'NULL'
        industry = labels_part[2] if len(labels_part) > 2 else labels_part[1]

        item_loader.add_value('size', size)
        item_loader.add_value('company_nature', labels_part[0])
        item_loader.add_value('industry', industry)

        info_part = re.sub('\s+', '', ''.join(str(response.css('.tBorderTop_box.bmsg .inbox p::text').extract())))
        res = re.match("(.*?)\(邮编：(.*)\)", info_part)
        if not res and info_part:
            address = info_part
        else:
            address = res.group(1)
        item_loader.add_value('address', address)
        item_loader.add_value('post_code', res.group(2) if res else 'NULL')
        item_loader.add_value('company_url', response.url)
        job51_item = item_loader.load_item()
        yield job51_item

