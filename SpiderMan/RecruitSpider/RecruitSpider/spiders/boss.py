import datetime
import time
import sys
from urllib import parse

import re
import scrapy
from scrapy.http import Request
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from RecruitSpider.items import BossItem, BossItemLoader
from tools.getFilterName import getAllCityName, getAllCityDataVal, getAllPositionType
from tools.seleniumTest import bossLogin

class BossSpider(scrapy.Spider):
    name = 'boss'
    start_urls = ['https://www.zhipin.com/']
    allowed_domains = ['wwww.zhipin.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 7,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10000,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        'DOWNLOAD_TIMEOUT': 200,
        'ITEM_PIPELINES' :{
            'RecruitSpider.pipelines.BossSpiderPipeline': 300,
        },
        # 'DOWNLOADER_MIDDLEWARES' : {
        #     'RecruitSpider.middlewares.MyProxiesSpiderMiddleware': 125,
        # },
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        'Connection': 'keep-alive',
        'Host': 'www.zhipin.com',
        'Referer': 'https://www.zhipin.com/job_detail/?query=&scity=101040100&industry=&position=100103',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }

    # 得到所有城市
    data_val = []
    # 得到所有职位的类型
    type = []
    types = getAllPositionType()
    for each in types:
        position_type = "".join(each)
        type.append(position_type)
    number = 0
    url_num = 0
    #抓取的城市的数量,北京为爬取的第一个城市
    n = 1
    # 当前城市停止标志 1:继续当前城市 2:下一个城市
    flag = 1
    cities = getAllCityName()
    for city_name in cities:
        # 得到城市编码
        city = "".join(city_name)
        num = "".join(getAllCityDataVal(city_name))
        data_val.append(num)


    def __init__(self, **kwargs):
        super(BossSpider, self).__init__()
        # 谷歌浏览器
        # 如果是linux环境 则开启无界面
        if 'linux' in sys.platform:
            from pyvirtualdisplay import Display
            self.display = Display(visible=0, size=(1024, 768))
            self.display.start()
        chrome_opt = Options()
        prefs = {"profile.managed_default_content_sttings.images": 2}  # 禁止图片加载
        chrome_opt.add_experimental_option("prefs", prefs)
        chrome_opt.add_argument("--no-sandbox")
        chrome_opt.add_argument("--disable-setuid-sandbox")
        self.browser = webdriver.Chrome(chrome_options=chrome_opt)

    # 爬虫信号绑定
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BossSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_close, signals.spider_closed)
        return spider

    def spider_close(self, spider):
        print('spider close')
        self.browser.quit()
        if 'linux' in sys.platform:
            self.display.stop()

    def start_requests(self):
        cookies = bossLogin('dict', self.browser)
        yield Request(url="https://www.zhipin.com/job_detail/?query="  + self.type[self.number] + "&scity=101010100&industry=&position=",cookies=cookies, headers=self.headers)

    def parse(self, response):
        if self.flag == 1:
            #从数据库的第一个城市，北京开始爬取
            yield Request(url=response.url , callback=self.parse_list, headers=self.headers, dont_filter=True)
        elif self.flag == 2:
            print("进入下一个城市")
            url = "https://www.zhipin.com/job_detail/?query=" + self.type[self.number] + "&scity=" + self.data_val[self.n] + "&industry=&position="
            time.sleep(5)
            yield Request(url=url, headers=self.headers, callback=self.parse_list, dont_filter=True)
            self.n += 1

    def parse_list(self, response):
        print("==============================职位列表页==============================")

        city = response.xpath('//span[@class="label-text"]/b/text()').extract_first()
        # 获取职位列表
        job_list = response.xpath('//div[@class="job-list"]/ul//li/div[@class="job-primary"]')
        for i in range(0, len(job_list)):
            item_loader = BossItemLoader(item=BossItem(), response=response)
            positionName = response.xpath('//div[@class="job-title"]/text()').extract()[i]
            positionUrl = response.xpath('//div[@class="info-primary"]/h3[@class="name"]/a/@href').extract()[i]
            companyUrl = response.xpath('//div[@class="company-text"]/h3[@class="name"]/a/@href').extract()[i]
            salary = response.xpath('//span[@class="red"]/text()').extract()[i]
            info_primary = response.css('div.info-primary > p::text').extract()
            workYear = info_primary[1]
            education = info_primary[2]
            companyUrl = parse.urljoin(response.url, companyUrl)
            positionUrl = parse.urljoin(response.url, positionUrl)

            item_loader.add_value('city', city)
            item_loader.add_value('positionName', positionName)
            item_loader.add_value('positionUrl', positionUrl)
            item_loader.add_value('companyUrl', str(companyUrl) if companyUrl else "NULL")
            item_loader.add_value('salary', salary)
            item_loader.add_value('workYear', workYear)
            item_loader.add_value('education', education)

            # 处理已经爬取过的页面
            fo = open('url.txt', 'r')
            get_url = fo.readlines()
            if len(get_url) == 0:
                with open('url.txt', 'a') as f:
                    f.write(positionUrl)
                    f.write("\n")
                    f.close()
                yield Request(url=positionUrl, headers=self.headers, meta={'item_loader': item_loader},
                              callback=self.position_detail, dont_filter=True)
            elif len(get_url) != 0:
                if self.url_num == len(get_url):
                    pass
                else:
                    for i in range(0, len(get_url)):
                        if get_url[i].strip('\n') == positionUrl:
                            # print("该网址已经爬取过了！")
                            break
                    else:
                        # print("该网址不存在！")
                        with open('url.txt', 'a') as f:
                            f.write("\n" + positionUrl)
                            f.close()
                            time.sleep(10)
                            yield Request(url=positionUrl, headers=self.headers, meta={'item_loader': item_loader},
                                          callback=self.position_detail, dont_filter=True)
        # 获取同一个城市下一页的链接
        next_page = response.css(".page a::attr(href)").extract()[-1]
        page = response.css('.page a:last-child::attr(class)').extract_first()
        if next_page != 'javascript:;':
            next_url = "https://www.zhipin.com/" + next_page
            time.sleep(10)
            yield Request(url=next_url, callback=self.parse_list, headers=self.headers, dont_filter=True)
        elif page == 'next disabled':
            self.number += 1
            yield Request(url="https://www.zhipin.com/job_detail/?query="  + self.type[self.number] +"&scity=" + self.data_val[self.n-1] + "&industry=&position=",
                          callback=self.parse_list, headers=self.headers, dont_filter=True)
            # 判断该城市所有职位页面是否已经爬取完
            if self.number == len(self.type) - 1:
                self.flag = 2
                yield Request(url='https://www.zhipin.com/', callback=self.parse, headers=self.headers, dont_filter=True)

    # 职位信息页
    def position_detail(self, response):
        print("==============================职位详情页==============================")
        url = re.match(r'https://www.zhipin.com/captcha/popUpCaptcha\?redirect=(.*?)', response.url)
        if url:
            print("出现验证码页，休息一下！")
            time.sleep(10)
        item_loader = response.meta.get('item_loader')
        jobTags = response.xpath('//div[@class="job-tags"]/span/text()').extract()
        content = response.xpath('//div[@class="job-sec"]/div[@class="text"]/text()').extract()
        location = response.xpath('//div[@class="location-address"]/text()').extract_first()
        companyShortName = response.xpath('//div[@class="info-company"]/h3[@class="name"]/a/text()').extract_first()
        company_infos = response.xpath('//div[@class="job-primary detail-box"]/div[@class="info-company"]/p/text()').extract()
        companyIndustry = response.xpath(
            '//div[@class="job-primary detail-box"]/div[@class="info-company"]/p/a/text()').extract_first()
        if companyIndustry is not None:
            companyIndustry = companyIndustry.strip()

        # 有的招聘这里只有两项，所以需判断
        if len(company_infos) >= 2:
            item_loader.add_value('companyFinanceStage', company_infos[0].strip())
            item_loader.add_value('companySize', company_infos[1].strip())
        elif len(company_infos) == 1:
            item_loader.add_value('companyFinanceStage', "NULL")
            item_loader.add_value('companySize', company_infos[0].strip())

        publishTime = response.xpath('//div[@class="job-author"]/span/text()').extract_first()
        if publishTime:
            # 处理日期
            if not publishTime.find('发布于'):
                pass
            publishTime = publishTime.replace("发布于", "")

        companyWebsite = response.xpath('//div[@class="info-company"]/p[2]/text()').extract_first()
        companyIntros = response.xpath('//div[@class="job-sec company-info"]/div[@class="text"]/text()').extract()
        companyIntro = (''.join(companyIntros).strip()).replace("'", "")  #将字符串里的"'"替换成""，避免插入数据库出错
        companyLogo = response.xpath('//div[@class="company-logo"]/a/img/@src').extract_first()
        companyFullName = response.xpath('//div[@class="job-sec"]/div[@class="name"]/text()').extract_first()
        companyResTime = response.xpath('//div[@class="job-sec"]/div[@class="level-list"]/li[@class="res-time"]/text()').extract_first()
        companyType = response.xpath('//div[@class="job-sec"]/div[@class="level-list"]/li[@class="company-type"]/text()').extract_first()

        item_loader.add_value('companyIndustry', companyIndustry if companyIndustry else "NULL")
        item_loader.add_value('publishTime', publishTime)
        item_loader.add_value('jobTags', str(','.join(jobTags)) if jobTags else "NULL")
        item_loader.add_value('content', str(''.join(content).strip()) if content else  "NULL")
        item_loader.add_value('location', location)
        item_loader.add_value('companyShortName',companyShortName)
        item_loader.add_value('companyWebsite', companyWebsite if companyWebsite else "NULL")
        item_loader.add_value('companyIntro', companyIntro if companyIntro else  "NULL")
        item_loader.add_value('companyLogo', companyLogo)
        item_loader.add_value('companyFullName', companyFullName if companyFullName else companyShortName)
        item_loader.add_value('companyResTime', companyResTime if companyResTime else "NULL")
        item_loader.add_value('companyType', companyType if companyType else "NULL")
        Boss_item = item_loader.load_item()
        yield Boss_item
