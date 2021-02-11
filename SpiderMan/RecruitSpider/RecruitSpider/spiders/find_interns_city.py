import scrapyfrom  RecruitSpider.items import FindInternsCityItemclass FindInternsCitySpider(scrapy.Spider):    name = 'findInternsCity'    start_urls = ['https://www.shixiseng.com/interns?']    allowed_domains = ['wwww.shixiseng.com']    custom_settings = {        'DOWNLOAD_DELAY': 3,        'ITEM_PIPELINES': {            'RecruitSpider.pipelines.InternsSpiderPipeline': 300,        },    }    headers = {        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",        "Accept-Encoding": "gzip, deflate, br",        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",        "Cache - Control": "max - age = 0",        'Connection': 'keep-alive',        'Cookie': 'SXS_XSESSION_ID="2|1:0|10:1521077606|15:SXS_XSESSION_ID|48:MTg5NmVhOTEtZmU0NC00NTk0LWFmYzEtMjFlNWZjMGI1YmZi|324103c8d11bf3882c2ff864ed5d0a8cb7e42558777d485cf421e538a282bcc1";'        'SXS_XSESSION_ID_EXP="2|1:0|10:1521077606|19:SXS_XSESSION_ID_EXP|16:MTUyMTE2NDAwNg==|e41d3e9cfcdd4595787d72d06ad1976c4e630ecbd65e4635596ec3ca06ba5e3d"; '        '__jsluid=92a7e5bb1052c0cafbfbf75563c33630;'        'uuid=a77d8e60-f03d-8ee1-8ae6-4db1bf48075d;'        'Hm_lvt_03465902f492a43ee3eb3543d81eba55=1521077807;'        'gr_user_id=b68acace-2414-42f7-a461-ab3eba054727;'        'MEIQIA_EXTRA_TRACK_ID=0z1EoLDhsQNJ1PnuGntqc7ubTLM;'        'search=; gr_session_id_96145fbb44e87b47=65c0a81a-403e-4c05-827b-b4195a0bd4cc;'        'gr_cs1_65c0a81a-403e-4c05-827b-b4195a0bd4cc=user_id%3Anull;'        'uid1=27451cff-000d-444f-95fc-0a53f449cea7; uid2=2a379ca3-706f-fbf3-ad13-ac6686173775;'        'SXS_VISIT_XSESSION_ID_V3.0="2|1:0|10:1521093042|26:SXS_VISIT_XSESSION_ID_V3.0|48:MTg5NmVhOTEtZmU0NC00NTk0LWFmYzEtMjFlNWZjMGI1YmZi|51c1cfdb22809d332e4c9d549aeb98231d77189fe15bd47d3570df461e71c068";'        'SXS_VISIT_XSESSION_ID_V3.0_EXP="2|1:0|10:1521093042|30:SXS_VISIT_XSESSION_ID_V3.0_EXP|16:MTUyMzY4NTA0Mg==|85b9f4c0e255d0acc3022921f05cc33eb5545a2c8633ef6616521e5a2f9b4171";'        'Hm_lpvt_03465902f492a43ee3eb3543d81eba55=1521093047',        'Host': 'www.shixiseng.com',        'Referer': 'https://www.shixiseng.com/',        'Upgrade-Insecure-Requests': 1,        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',    }    def parse(self,response):        cities =response.xpath(            '//div[@class="cover"]/div[@class="city-box"]/div[@class="city-list"]/ul[@class="more-city"]//ul[@class="list-item clearfix"]/li')        for eachCity in cities:            item = FindInternsCityItem()            city_name = eachCity.css('li::text').extract_first()            data_val = eachCity.css('li::attr(data-val)').extract_first()            print(city_name)            item['cityName'] = city_name            item['dataVal'] = data_val            yield item