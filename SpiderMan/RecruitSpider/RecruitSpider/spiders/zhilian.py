# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import signals
from tools.getFilterName import getCityPinYin
from RecruitSpider.items import ZhilianItemLoader, ZhilianItem
from urllib import parse as ps
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tools.seleniumTest import platformJudge
import sys

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://jobs.zhaopin.com/']

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2,
        'ITEM_PIPELINES': {
            'RecruitSpider.pipelines.ZhilianSpiderPipeline': 300,
        },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'RecruitSpider.middlewares.RandomUserAgentMiddleware': 543,
        # },
        # 'CONCURRENT_REQUESTS': 1,
        'HTTPERROR_ALLOWED_CODES': [500, 404, 504],
    }

    headers = {
        'Host': 'jobs.zhaopin.com',
        'Referer': 'http://jobs.zhaopin.com/beijing/',
        'Origin': 'http://jobs.zhaopin.com/',
        'Cache_Control': "max-age=0",
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
    }
    # 当前抓取城市数量
    n = 0
    total_city_pinyin = getCityPinYin()

    # 过滤错误拼音
    total_city_pinyin.append('chongqing')
    total_city_pinyin.remove('zhongqing')
    total_city_num = len(total_city_pinyin)
    err_num = 0

    # ******************************************开启 Selenium 配置***********************************************

    def __init__(self, **kwargs):
        super(ZhilianSpider, self).__init__()
        # 谷歌浏览器
        # 如果是linux环境 则开启无界面
        if 'linux' in sys.platform:
            from pyvirtualdisplay import Display
            self.display = Display(visible=0,size=(1024,768))
            self.display.start()

        chrome_opt = Options()
        prefs = {"profile.managed_default_content_sttings.images": 2}
        chrome_opt.add_experimental_option("prefs", prefs)
        chrome_opt.add_argument("--no-sandbox")
        chrome_opt.add_argument("--disable-setuid-sandbox")

        driver_path = platformJudge()
        self.browser = webdriver.Chrome(driver_path, chrome_options=chrome_opt)

    # 爬虫信号绑定
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ZhilianSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_close, signals.spider_closed)
        return spider

    def spider_close(self, spider):
        print('spider close')
        self.browser.quit()
        if 'linux' in sys.platform:
            self.display.stop()

    # *****************************************************************************************************

    def start_requests(self):
        # 组建爬取城市链接
        # for item in self.total_city_pinyin:
        #     yield Request(ps.urljoin('http://jobs.zhaopin.com', item), headers=self.headers, meta={'err_num': 0})
        yield Request(ps.urljoin('http://jobs.zhaopin.com', 'chengdu'), headers=self.headers, meta={})

    def parse(self, response):
        # 获取当前页数
        page_obj = re.match(r"http://.*?/.*?/p(\d*)/$", response.url)
        page_num = page_obj.group(1) if page_obj else 1
        # 遇到500页面爬取下一页
        if response.status in (500, 404, 504):
            print('去你妹的! 第' + str(page_num) + '页')
            sleep(2)
            self.err_num += 1
            if self.err_num % 5 == 0:
                yield Request(ps.urljoin('http://jobs.zhaopin.com', self.total_city_pinyin[self.n]), headers=self.headers)
                self.n += 1
            else:
                page_num = int(page_num) + 1
                next_url = re.sub(r'\d+', str(page_num), response.url)
                yield Request(url=ps.urljoin(response.url, next_url), headers=self.headers, meta={'err_num': err_num}, callback=self.parse)
        else:
            self.headers['Referer'] = response.url
            # 获取职位列表
            position_list = response.xpath("//div[contains(@class,'details_container')]")

            print( '总进度：' + str(self.n + 1) + '/' + str(self.total_city_num) + position_list[0].xpath("span[contains(@class,'address')]/text()").extract_first() + " 第" + str(page_num) + "页")

            # 判断如果有职位信息
            if len(position_list) > 0:
                for position_node in position_list:
                    # 职位详情页
                    position_url = position_node.xpath("span[contains(@class,'post')]/a/@href").extract_first()
                    # 公司工商信息详情页
                    company_url = position_node.xpath("span[contains(@class,'company_name')]/a/@href").extract_first()
                    # 不使用selenium 抓取
                    yield Request(url=ps.urljoin(response.url, position_url), headers=self.headers, meta={'company_url': company_url}, callback=self.position_detail)
            # 获取下一页
            next_url = response.xpath("//div[@class='searchlist_page']/span[@class='search_page_next']/a/@href").extract_first()
            if next_url:
                yield Request(url=ps.urljoin(response.url, next_url), headers=self.headers, meta={'err_num': self.err_num}, callback=self.parse)
            else:
                yield Request(url=ps.urljoin('http://jobs.zhaopin.com', self.total_city_pinyin[self.n]), headers=self.headers ,callback=self.parse)
                self.n += 1

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

            industry = response.xpath("//div[contains(@class,'company-box')]/ul/li[3]/strong/a/text()").extract_first()
            item_loader.add_value('industry', industry if industry else "NULL")

            if len(response.xpath("//div[contains(@class,'company-box')]/ul/li")) == 5:
                item_loader.add_xpath('website', "//div[contains(@class,'company-box')]/ul/li[4]/strong/a/text()")
                # 需要二次处理字段，原因：去掉空白字符和换行符
                company_address = re.sub(r'\s+', '', response.xpath("//div[contains(@class,'company-box')]/ul/li[5]/strong/text()").extract_first())
                item_loader.add_value('address', company_address if company_address else 'NULL')
            else:
                item_loader.add_value('website', "NULL")
                # 需要二次处理字段，原因：去掉空白字符和换行符
                company_address = re.sub(r'\s+', '', response.xpath("//div[contains(@class,'company-box')]/ul/li[4]/strong/text()").extract_first())
                item_loader.add_value('address', company_address if company_address else 'NULL')

            item_loader.add_value('company_url', response.meta.get("company_url"))

            # 智联招聘职位zhilian_position item
            item_loader.add_xpath('position_name', "//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/h1/text()")
            item_loader.add_xpath('salary_low', "//div[contains(@class,'terminalpage-left')]/ul/li[1]/strong/text()")
            item_loader.add_xpath('salary_high', "//div[contains(@class,'terminalpage-left')]/ul/li[1]/strong/text()")
            item_loader.add_xpath('city', "//div[contains(@class,'terminalpage-left')]/ul/li[2]/strong/a/text()")
            publish_time = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[3]/strong/span/text()").extract_first()
            item_loader.add_value('publish_time', publish_time if publish_time else 'NULL')
            item_loader.add_xpath('job_nature', "//div[contains(@class,'terminalpage-left')]/ul/li[4]/strong/text()")
            item_loader.add_xpath('work_year', "//div[contains(@class,'terminalpage-left')]/ul/li[5]/strong/text()")
            item_loader.add_xpath('education', "//div[contains(@class,'terminalpage-left')]/ul/li[6]/strong/text()")

            # 需要二次处理字段， 原因：去掉人数的人字
            item_loader.add_xpath('recruit_num', "//div[contains(@class,'terminalpage-left')]/ul/li[7]/strong/text()")
            item_loader.add_xpath('position_type', "//div[contains(@class,'terminalpage-left')]/ul/li[8]/strong/a/text()")
            # 需要二次处理字段。 原因：md5

            publish_time = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[3]/strong/span/text()").extract_first()
            unique_md5 = response.xpath("//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/h1/text()").extract_first() + company_name + publish_time if publish_time else '失效'
            item_loader.add_value('unique_md5', unique_md5)

            content_obj = response.xpath("//div[contains(@class,'terminalpage-main')]/div[contains(@class,'tab-cont-box')]/div[1]")
            content_arr = content_obj.xpath("p[position() < last()]").extract() + content_obj.xpath("div/p[position() < last()]").extract()
            if not content_arr:
                content_arr = content_obj.xpath("div").extract()
            item_loader.add_value('content', ''.join(content_arr) if content_arr else "NULL")

            # 需要二次处理字段 原因：去掉空白字符和换行符
            item_loader.add_xpath('location', "//div[contains(@class,'terminalpage-main')]/div[contains(@class,'tab-cont-box')]/div[1]/h2/text()")
            item_loader.add_value('url', response.url)
            # 需要二次处理字段 原因：数组
            advantage_labels = ','.join(response.xpath("//div[contains(@class,'top-fixed-box')]/div[contains(@class,'fixed-inner-box')]/div[contains(@class,'inner-left')]/div[contains(@class,'welfare-tab-box')]/span/text()").extract())
            item_loader.add_value('advantage_labels', advantage_labels if advantage_labels else "NULL")

            position_detail_item = item_loader.load_item()
            yield position_detail_item