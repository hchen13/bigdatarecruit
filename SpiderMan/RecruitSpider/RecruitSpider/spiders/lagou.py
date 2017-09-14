# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
from urllib import parse
from SpiderMan.RecruitSpider.RecruitSpider.items import LagouItem,LagouItemLoader
from SpiderMan.RecruitSpider.tools.seleniumTest import lagouLogin
import json
import requests
import time

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/allCity.html?px=new&city=%E5%8C%97%E4%BA%AC']

    headers = {
        "HOST": "www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_?&px=new&city=%E5%8C%97%E4%BA%AC",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    }

    def start_requests(self):
        cookies = lagouLogin('dict')
        yield Request('https://www.lagou.com/jobs/allCity.html?px=new&city=%E5%8C%97%E4%BA%AC',cookies=cookies)

    # 进入城市列表
    def parse(self, response):
        city_parent = response.xpath("//table[contains(@class,'word_list')]/tr")

        for city_node in city_parent:
            city_initial = city_node.xpath("td[1]/div/span/text()").extract_first()
            city_initial_part = city_node.xpath("td[2]/ul/li")
            city_total_num = len(city_parent.xpath("td[2]/ul/li"))
            for city_part in city_initial_part :
                city_name = city_part.xpath('a/text()').extract_first()
                url = city_part.xpath('input/@value').extract_first()
                if city_name == "上海":
                    yield Request(url=parse.urljoin(response.url,url), meta={'city_name':city_name,'city_initial':city_initial,'city_total_num':city_total_num,'curNum':1}, callback=self.positionList)

    # 进入职位列表页
    def positionList(self,response):
        # 组装接口链接
        city_str = {"city": response.meta.get('city_name')}
        url_city_str = parse.urlencode(city_str)
        url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&' + url_city_str + '&needAddtionalResult=false&isSchoolJob=0'

        curNum = response.meta.get('curNum')
        query_data = {'first': 'false', 'pn': curNum, 'kd': ''}

        if curNum == 1:
            res = requests.post(url=url, headers=self.headers, data=query_data).json()
        else:
            res = json.loads(response.body)
        if res["success"] and res['content']['pageNo'] != 0:
            hrInfoMap = res['content']['hrInfoMap']
            positionResult = res['content']['positionResult']['result']
            totalNum = res['content']['positionResult']['totalCount']

            print(response.meta.get('city_name') + " 职位总数：" + str(totalNum))

            # for item in positionResult:
            #     # 如果不是今天发布的，则跳过
            #     t = time.strptime(item['createTime'], "%Y-%m-%d %H:%M:%S")
            #     date_cur = t[0] *10000 + t[1] * 100 + t[2]
            #     date_cur_comp = int(time.strftime('%Y%m%d', time.localtime()))
            #     # 2为当天 1为全部
            #     status = 2 if date_cur == date_cur_comp else 1
            #     if status:
            #         url_detail = "https://www.lagou.com/jobs/" + str(item["positionId"]) + '.html'
            #         positionId = str(item["positionId"])
            #         hrInfo = hrInfoMap[positionId]
            #         yield Request(url=url_detail, meta={"hrInfoMap": hrInfo,'positionInfo':item, 'city_initial':response.meta.get('city_initial'), 'total_num':totalNum}, callback=self.positionDetail)
            curNum = res['content']['pageNo'] + 1
            query_data = {'first': 'false', 'pn': str(curNum), 'kd': ''}
            return FormRequest(url=url,callback=self.positionList,formdata=query_data,method="POST",meta={"curNum":curNum,'city_name':response.meta.get('city_name')})


    # 职位详情页
    def positionDetail(self,response):
        item_loader = LagouItemLoader(item=LagouItem(),response=response)
        positionInfo = response.meta.get('positionInfo')
        hrInfo = response.meta.get('hrInfoMap')

        print(positionInfo['city'] + '： ' + positionInfo['positionName'])

        item_loader.add_value('cityInitial',response.meta.get('city_initial'))
        item_loader.add_value('cityTotalNum',response.meta.get('total_num'))

        item_loader.add_value('url', response.url)
        item_loader.add_value('positionName',positionInfo['positionName'])
        item_loader.add_value('positionId', positionInfo['positionId'])
        item_loader.add_value('positionLabels', positionInfo['positionLables'] if positionInfo['positionLables'] else 'NULL')
        item_loader.add_value('salary', positionInfo['salary'])
        item_loader.add_value('workYear', positionInfo['workYear'])
        item_loader.add_value('education', positionInfo['education'])
        item_loader.add_value('jobNature', positionInfo['jobNature'])
        item_loader.add_value('firstType', positionInfo['firstType'])
        item_loader.add_value('secondType', positionInfo['secondType'])
        item_loader.add_value('city', positionInfo['city'])
        item_loader.add_value('district', positionInfo['district'] if positionInfo['district'] else 'NULL')

        item_loader.add_value('companyId', positionInfo['companyId'])
        item_loader.add_value('companyFullName', positionInfo['companyFullName'])
        item_loader.add_value('companyShortName', positionInfo['companyShortName'])
        item_loader.add_value('companySize', positionInfo['companySize'] if positionInfo['companySize'] else 'NULL')
        item_loader.add_value('companyLogo', 'https://www.lagou.com/' + positionInfo['companyLogo'])
        item_loader.add_value('industryField', positionInfo['industryField'] if positionInfo['industryField'] else 'NULL')
        item_loader.add_value('financeStage', positionInfo['financeStage'] if positionInfo['financeStage'] else 'NULL')

        item_loader.add_value('publisherId', positionInfo['publisherId'])
        item_loader.add_value('publishTime', positionInfo['createTime'])
        item_loader.add_value('positionAdvantage', positionInfo['positionAdvantage'])
        item_loader.add_value('location', response.xpath("//div[@class='work_addr']").xpath('string(.)').extract_first())
        item_loader.add_xpath('department', "//div[@class='company']/text()")
        item_loader.add_css('describe', '.job_bt div')

        item_loader.add_value('hrPortrait', hrInfo['portrait'] if hrInfo['portrait'] else 'NULL')
        item_loader.add_value('hrPositionName', hrInfo['positionName'] if hrInfo['positionName'] else 'NULL')
        item_loader.add_value('hrRealName', hrInfo['realName'])
        item_loader.add_xpath('hrActiveTime', "//div[@class='publisher_data']/div[3]/span[3]/text()")
        hr_connect_url = "https://www.lagou.com/scanCode/positionChat.html?positionId={0}&publishUserId={1}".format(positionInfo['positionId'],positionInfo['publisherId'])
        item_loader.add_value('hrConnectionLagou', hr_connect_url)
        lagou_item = item_loader.load_item()
        yield lagou_item