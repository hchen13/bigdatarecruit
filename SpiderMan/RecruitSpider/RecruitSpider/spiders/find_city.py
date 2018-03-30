import scrapy

from RecruitSpider.items import FindCityItem


class FindCitySpider(scrapy.Spider):
    name = 'findCity'
    start_urls = ['https://www.zhipin.com/job_detail/?ka=header-job']
    allowed_domains = ['wwww.zhipin.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {
            'RecruitSpider.pipelines.BossSpiderPipeline': 300,
        },
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        'Connection': 'keep-alive',
        'Cookie': '__c = 1517195881;JSESSIONID = ""; __g = -;Hm_lvt_194df3105ad7148dcf2b98a91b5e727a = 1517195885;'
                  '__l = r = https % 3A % 2F % 2Fwww.google.co.jp % 2F & l = % 2F;'
                  'toUrl = https % 3A % 2F % 2Fwww.zhipin.com % 2Fjob_detail % 2F1416590963.html % 3ka % 3Dsearch_list_31;'
                  'lastCity = 100010000;Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a = 1517295824;__a = 62158117.1517195881..1517195881.124.1.124.124',
        'Host': 'www.zhipin.com',
        'Referer': 'https://www.zhipin.com/job_detail/?query=&scity=101040100&industry=&position=100103',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }

    def parse(self,response):
        cities= response.xpath('//div[@class="dorpdown-city"]//li')
        print(cities)
        for eachCity in cities:
            item = FindCityItem()
            city_name = eachCity.css('li::text').extract_first()
            data_val = eachCity.css('li::attr(data-val)').extract_first()
            print(city_name)
            item['cityName'] = city_name
            item['dataVal'] = data_val
            yield item
