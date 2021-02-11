import scrapy

from RecruitSpider.items import FindPositionTypeItem


class FindPositionTypeSpider(scrapy.Spider):
    name = 'positionType'
    start_urls = ['https://www.zhipin.com']
    allowed_domains = ['wwww.zhipin.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
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

    def parse(self, response):
        position_tag = []
        parent_tag = []
        parentTages = []

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[1]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[2]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[2]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[3]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[3]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[4]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[4]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)
        print(position_tag)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[5]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[5]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[6]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[6]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[7]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[7]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[8]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[8]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/dl[9]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[1]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[1]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[4]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[4]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[5]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[5]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[7]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[7]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[8]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[8]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[9]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[9]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[10]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[10]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        length = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li/div[@class="text"]/a').extract())
        positionTags = response.xpath('//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/dd/a/text()').extract()
        for i in range(0, length):
            position_tag.append(positionTags)

        parentTags = response.xpath('//div[@class="job-menu"]//dl/div[@class="menu-sub"]/ul//li')
        for eachTag in parentTags:
            parentTag = eachTag.xpath('h4/text()').extract_first()
            parentTages.append(parentTag)

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[0])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[1])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[2])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[3])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[4])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[5])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[7]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[6])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[8]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[7])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[9]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[8])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[10]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[9])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[11]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[10])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[12]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[11])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[13]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[12])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[1]/div[@class="menu-sub"]/ul/li[14]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[13])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[2]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[14])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[2]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[15])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[2]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[16])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[3]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[17])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[3]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[18])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[3]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[19])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[3]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[20])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[3]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[21])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[3]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[22])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[4]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[23])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[4]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[24])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[4]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[25])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[4]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[26])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[4]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[27])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[5]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[28])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[5]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[29])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[5]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[30])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[5]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[31])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[5]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[32])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[5]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[33])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[6]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[34])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[6]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[35])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[6]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[36])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[6]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[37])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[6]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[38])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[6]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[39])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[7]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[40])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[7]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[41])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[7]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[42])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[8]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[43])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[8]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[44])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[8]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[45])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[8]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[46])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[8]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[47])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[8]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[48])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[49])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[50])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[51])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[52])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[53])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[54])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[7]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[55])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/dl[9]/div[@class="menu-sub"]/ul/li[8]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[56])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[1]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[57])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[1]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[58])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[1]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[59])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[60])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[61])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[62])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[63])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[64])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[65])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[7]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[66])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[2]/div[@class="menu-sub"]/ul/li[8]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[67])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[68])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[69])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[70])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[71])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[72])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[73])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[7]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[74])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[3]/div[@class="menu-sub"]/ul/li[8]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[75])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[4]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[76])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[4]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[77])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[4]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[78])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[5]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[79])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[5]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[80])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[5]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[81])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[5]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[82])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[5]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[83])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[84])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[85])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[86])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[87])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[88])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[6]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[89])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[7]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[90])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[7]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[91])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[7]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[92])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[7]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[93])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[7]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[94])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[8]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[95])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[8]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[96])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[9]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[97])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[9]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[98])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[9]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[99])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[10]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[100])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[10]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[101])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[10]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[102])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[10]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[103])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li[1]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[104])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li[2]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[105])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li[3]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[106])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li[4]/div[@class="text"]/a').extract())

        for i in range(0, par_len):
            parent_tag.append(parentTages[107])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li[5]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[108])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li[6]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[109])

        par_len = len(response.xpath(
            '//div[@class="job-menu"]/div[@class="all-box"]/dl[11]/div[@class="menu-sub"]/ul/li[7]/div[@class="text"]/a').extract())
        for i in range(0, par_len):
            parent_tag.append(parentTages[110])

        num = response.xpath('//div[@class="job-menu"]//dl//div[@class="menu-sub"]/ul//li/div[@class="text"]/a')
        for i in range(0, len(num)):
            item = FindPositionTypeItem()
            positionType = response.xpath(
                '//div[@class="job-menu"]//dl/div[@class="menu-sub"]/ul//li/div[@class="text"]/a/text()').extract()[i]
            item['positionType'] = positionType
            item['positionTag'] = "/".join(position_tag[i])
            item['parentTag'] = parent_tag[i]
            yield item