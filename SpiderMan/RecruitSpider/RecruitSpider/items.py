# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose , Join
import time
from RecruitSpider.helper import md5
import re

class RecruitspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

# 去掉空白字符
def RemoveBlankCharacter(value):
    return re.sub(r'\s+', '', value)

# 处理拉钩工作地址
def locationDeal(value):
    return value.replace("查看地图","")


class LagouItem(scrapy.Item):

    cityInitial = scrapy.Field()
    cityTotalNum = scrapy.Field()
    url = scrapy.Field()
    positionName = scrapy.Field()
    positionId = scrapy.Field()
    positionLabels = scrapy.Field(
        output_processor=Join(",")
    )
    salary = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    jobNature = scrapy.Field()
    firstType = scrapy.Field()
    secondType = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()

    companyId = scrapy.Field()
    companyFullName = scrapy.Field()
    companyShortName = scrapy.Field()
    companySize = scrapy.Field()
    companyLogo = scrapy.Field()
    industryField = scrapy.Field(
        output_processor=Join(",")
    )
    financeStage = scrapy.Field()

    publisherId = scrapy.Field()
    publishTime = scrapy.Field()
    positionAdvantage = scrapy.Field()
    location = scrapy.Field(
        input_processor=MapCompose(locationDeal,RemoveBlankCharacter),
    )
    department = scrapy.Field()
    describe = scrapy.Field()

    hrPortrait = scrapy.Field()
    hrRealName = scrapy.Field()
    hrActiveTime = scrapy.Field()
    hrConnectionLagou = scrapy.Field()
    hrPositionName = scrapy.Field()

    state = scrapy.Field()
    endTime = scrapy.Field()

    def get_company_insert_sql(self):

        insert_sql = """
            insert into lagou_company(
            company_id,
            full_name,
            short_name,
            size,
            logo,
            industry,
            finance_stage,
            created_at,
            num
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now()),num=num+1
        """
        params = (self['companyId'], self['companyFullName'], self['companyShortName'], self['companySize'],self['companyLogo'],self['industryField'],self['financeStage'],int(time.time()),1)
        return insert_sql,params

    def get_hr_insert_sql(self):

        try:
            hrActiveTime = self['hrActiveTime']
        except Exception as e:
            hrActiveTime = None

        insert_sql = """
            insert into lagou_hr(
            publisher_id,
            position_name,
            portrait,
            real_name,
            position_id,
            active_time,
            connection_lagou,
            created_at,
            num
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now()),num=num+1
        """
        params = (self['publisherId'], self['hrPositionName'], self['hrPortrait'], self['hrRealName'], self['positionId'],hrActiveTime, self['hrConnectionLagou'], int(time.time()),1)
        return insert_sql, params

    def  get_recruit_day_update_sql(self):
        update_sql = """
                update lagou_recruit_day set state = %d, end_time = '%s' where url = '%s'  
        """ %(self['state'], self['endTime'], self['url'])
        return update_sql

    def get_recruit_day_insert_sql(self):

        try:
            department = self['department']
        except Exception as e:
            department = None

        insert_sql = """
            insert into lagou_recruit_day(
            position_id,
            url,
            position_name,
            position_labels,
            salary,
            work_year,
            education,
            job_nature,
            first_type,
            second_type,
            city,
            district,
            company_id,
            position_advantage,
            location,
            publisher_id,
            publish_time,
            department,
            content,
            created_at
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
        """
        params = (self['positionId'], self['url'] , self['positionName'], self['positionLabels'], self['salary'], self['workYear'], self['education'], self['jobNature'], self['firstType'], self['secondType'],self['city'], self['district'], self['companyId'], self['positionAdvantage'], self['location'], self['publisherId'], self['publishTime'], department, self['describe'], int(time.time()))
        return insert_sql, params

    def get_city_insert_sql(self):
        import time

        insert_sql = """
            insert into lagou_city(
            city_name,
            name_initial,
            created_at,
            num,
            total_num
            ) 
            values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now()),num=num+1,total_num=VALUES(total_num)
        """
        params = (self['city'], self['cityInitial'], int(time.time()),1,self['cityTotalNum'])
        return insert_sql, params


def getSalaryLow(value):
    salary_obj = re.match(r"([\d]+)-([\d]+)元", value)
    if salary_obj:
        return salary_obj.group(1)
    else:
        return 0

def getSlaryHigh(value):
    salary_obj = re.match(r"([\d]+)-([\d]+)元", value)
    if salary_obj:
        return salary_obj.group(2)
    else:
        return 0

def getRecruitNum(value):
    res = re.match(r'\d+',value)
    if res:
        return re.sub('人', '', value)
    else:
        return 0


class ZhilianItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ZhilianItem(scrapy.Item):
    # 公司zhilian_company item
    company_md5 = scrapy.Field(
        input_processor=MapCompose(md5),
    )
    full_name = scrapy.Field()
    size = scrapy.Field()
    company_nature = scrapy.Field()
    logo = scrapy.Field()
    website = scrapy.Field()
    industry = scrapy.Field()
    address = scrapy.Field(
        input_processor=MapCompose(RemoveBlankCharacter),
    )
    company_url = scrapy.Field()

    # 智联招聘职位zhilian_position item
    position_name = scrapy.Field()
    city = scrapy.Field()
    unique_md5 = scrapy.Field(
        input_processor=MapCompose(md5),
    )
    salary_low = scrapy.Field(
        input_processor=MapCompose(getSalaryLow),
    )
    salary_high = scrapy.Field(
        input_processor=MapCompose(getSlaryHigh),
    )
    location = scrapy.Field(
        input_processor=MapCompose(RemoveBlankCharacter),
    )
    publish_time = scrapy.Field()
    advantage_labels = scrapy.Field()
    job_nature = scrapy.Field()
    work_year = scrapy.Field()
    education = scrapy.Field()
    recruit_num = scrapy.Field(
        input_processor=MapCompose(getRecruitNum),
    )
    position_type = scrapy.Field()
    content =scrapy.Field()
    url = scrapy.Field()

    state = scrapy.Field()
    endTime = scrapy.Field()

    def get_zhilian_company_insert_sql(self):

        insert_sql = """
            insert into zhilian_company(
            company_md5,
            full_name,
            size,
            company_nature,
            logo,
            website,
            industry,
            address,
            created_at,
            company_url
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
        """
        params = (self['company_md5'], self['full_name'], self['size'], self['company_nature'], self['logo'], self['website'], self['industry'], self['address'], int(time.time()), self['company_url'])
        return insert_sql, params

    def get_zhilian_position_update_sql(self):
        update_sql = """
                        update zhilian_position set state = %d, end_time = '%s' where url = '%s'  
                """ % (self['state'], self['endTime'], self['url'])
        return update_sql

    def get_zhilian_position_insert_sql(self):

        insert_sql = """
            insert into zhilian_position(
            position_name,
            city,
            company_md5,
            unique_md5,
            salary_low,
            salary_high,
            location,
            publish_time,
            advantage_labels,
            job_nature,
            work_year,
            education,
            recruit_num,
            position_type,
            content,
            url,
            created_at
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
        """
        params = (self['position_name'], self['city'], self['company_md5'], self['unique_md5'], self['salary_low'], self['salary_high'], self['location'], self['publish_time'], self['advantage_labels'], self['job_nature'], self['work_year'], self['education'], self['recruit_num'], self['position_type'], self['content'], self['url'], int(time.time()))
        return insert_sql, params


class Job51ItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def removeStr(value):
    return re.sub('工作|经验', '', value)


class Job51PositionItem(scrapy.Item):
    # 51job city item
    city_name = scrapy.Field()
    city_code = scrapy.Field()

    # 51job position item
    name = scrapy.Field()
    district = scrapy.Field()
    salary = scrapy.Field()
    company_md5 = scrapy.Field(
        input_processor=MapCompose(md5),
    )
    work_year = scrapy.Field(
        input_processor=MapCompose(removeStr),
    )
    education = scrapy.Field()
    recruit_num = scrapy.Field()
    publish_time = scrapy.Field()
    language = scrapy.Field()
    industry = scrapy.Field()
    position_labels = scrapy.Field(
        output_processor=Join(",")
    )
    advantage = scrapy.Field(
        output_processor=Join(",")
    )
    content = scrapy.Field()
    location = scrapy.Field()
    phone_num = scrapy.Field()
    email = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field(
        input_processor=MapCompose(md5),
    )

    state = scrapy.Field()
    endTime = scrapy.Field()
    year = scrapy.Field()

    def get_51Job_position_update_sql(self):
        update_sql = """
                update 51job_position set state = %d, end_time = '%s' where url = '%s'
        """%(self['state'], self['endTime'], self['url'])
        return update_sql

    def get_51Job2017_position_update_sql(self):
        update_sql = """
                  update 51job_position_2017 set state = %d, end_time = '%s' where url = '%s'
          """ % (self['state'], self['endTime'], self['url'])
        return update_sql
    def get_51Job_city_insert_sql(self):

        insert_sql = """
            insert into 51job_city(
            city_name,
            city_code,
            num,
            created_at
            ) 
            values(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now()),num=num+1
        """
        params = (self['city_name'], self['city_code'], 1, int(time.time()))
        return insert_sql, params

    def get_51Job_position_insert_sql(self):

        insert_sql = """
            insert into 51job_position(
            name,
            city,
            district,
            salary,
            company_md5,
            work_year,
            education,
            recruit_num,
            publish_time,
            language,
            industry,
            position_labels,
            advantage,
            content,
            location,
            phone_num,
            email,
            url,
            url_md5,
            created_at
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
        """
        params = (self['name'],
                  self['city_name'],
                  self['district'],
                  self['salary'],
                  self['company_md5'],
                  self['work_year'],
                  self['education'],
                  self['recruit_num'],
                  self['publish_time'],
                  self['language'],
                  self['industry'],
                  self['position_labels'],
                  self['advantage'],
                  self['content'],
                  self['location'],
                  self['phone_num'],
                  self['email'],
                  self['url'],
                  self['url_md5'],
                  int(time.time()))

        return insert_sql, params

class Job51CompanyItem(scrapy.Item):
    # 公司zhilian_company item
    company_md5 = scrapy.Field(
        input_processor=MapCompose(md5),
    )
    full_name = scrapy.Field()
    size = scrapy.Field()
    company_nature = scrapy.Field()
    industry = scrapy.Field()
    address = scrapy.Field(
        input_processor=MapCompose(RemoveBlankCharacter),
    )
    company_url = scrapy.Field()
    post_code = scrapy.Field()

    def get_51Job_company_insert_sql(self):
        insert_sql = """
            insert into 51job_company(
            company_md5,
            full_name,
            size,
            company_nature,
            industry,
            address,
            company_url,
            postcode,
            num,
            created_at
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now()),num=num+1
        """
        params = (
        self['company_md5'],
        self['full_name'],
        self['size'],
        self['company_nature'],
        self['industry'],
        self['address'],
        self['company_url'],
        self['post_code'],
        1,
        int(time.time()))
        return insert_sql, params

class FindCityItem(scrapy.Item):
    # 城市信息 item
    cityName = scrapy.Field()
    dataVal = scrapy.Field()

    def get_findCity_insert_sql(self):
        insert_sql = """
                 INSERT INTO boss_city(
                 city_name,
                 data_val,
                 created_at)
                 VALUES('%s', '%s', '%s')ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
                 """ %(self['cityName'], self['dataVal'], int(time.time()))
        return insert_sql

class FindPositionTypeItem(scrapy.Item):
    # 职位类型 item
    positionType = scrapy.Field()
    positionTag = scrapy.Field()
    parentTag = scrapy.Field()

    @property
    def get_findPositionType_insert_sql(self):
        insert_sql = """
                 INSERT INTO boss_position_type(
                 position_type,
                 position_tag,
                 parent_tag,
                 created_at)
                 VALUES('%s', '%s', '%s', '%s')ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
                 """ %(self['positionType'], self['positionTag'], self['parentTag'], int(time.time()))
        return insert_sql

class BossItemLoader(ItemLoader):
        default_output_processor = TakeFirst()

class BossItem(scrapy.Item):
    # 公司信息 item
    companyShortName = scrapy.Field()
    companyFullName = scrapy.Field()
    companySize = scrapy.Field()
    companyLogo = scrapy.Field()
    companyFinanceStage = scrapy.Field()
    companyWebsite = scrapy.Field()
    companyType = scrapy.Field()
    companyResTime = scrapy.Field()
    companyIndustry = scrapy.Field()
    companyUrl = scrapy.Field()
    companyIntro = scrapy.Field()

    # 招聘职位的信息 item
    positionName = scrapy.Field()
    publishTime = scrapy.Field()
    salary = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    jobTags = scrapy.Field()
    content = scrapy.Field()
    city = scrapy.Field()
    location = scrapy.Field()
    positionUrl = scrapy.Field()

    def get_boss_company_insert_sql(self):
        insert_sql = """
                    INSERT INTO boss_company(
                    short_name,
                    full_name,
                    size,
                    logo,
                    finance_stage,
                    website,
                    company_type,
                    res_time,
                    created_at,
                    industry,
                    company_url,
                    intro
                    )
                    VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
                """ % (self['companyShortName'], self['companyFullName'], self['companySize'], self['companyLogo'],
                       self['companyFinanceStage'], self['companyWebsite'], self['companyType'], self['companyResTime'],
                       int(time.time()), self['companyIndustry'], self['companyUrl'], self['companyIntro'])
        return insert_sql

    def get_boss_position_insert_sql(self):
        insert_sql = """
                    insert into boss_position(
                    position_name,
                    publish_time,
                    salary,
                    work_year,
                    education,
                    job_tags,
                    content,
                    city,
                    location,
                    position_url,
                    created_at
                    )
                    VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
                """ % (self['positionName'], self['publishTime'], self['salary'], self['workYear'], self['education'],
                       self['jobTags'], self['content'], self['city'], self['location'], self['positionUrl'],
                       int(time.time()))
        return insert_sql

class FindInternsCityItem(scrapy.Item):
    # 城市信息 item
    cityName = scrapy.Field()
    dataVal = scrapy.Field()

    def get_findInternsCity_insert_sql(self):
        insert_sql = """
                 INSERT INTO interns_city(
                 city_name,
                 data_val,
                 created_at)
                 VALUES('%s', '%s', '%s')ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
                 """ %(self['cityName'], self['dataVal'], int(time.time()))
        return insert_sql

#     实习僧的Item

class InternItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class InternPositionItem(scrapy.Item):

    # 招聘职位
    positionName = scrapy.Field()
    month = scrapy.Field()
    maxsal = scrapy.Field()
    com_logo = scrapy.Field()
    minsal = scrapy.Field()
    city = scrapy.Field()
    com_scale = scrapy.Field()
    reslan = scrapy.Field()
    attraction = scrapy.Field()
    ftype = scrapy.Field()
    collected = scrapy.Field()
    cuuid = scrapy.Field()
    degree = scrapy.Field()
    delivered = scrapy.Field()
    chance = scrapy.Field()
    work_address = scrapy.Field()
    endtime = scrapy.Field()
    day = scrapy.Field()
    work_info = scrapy.Field()
    positionUrl = scrapy.Field()
    com_industry = scrapy.Field()
    refresh = scrapy.Field()
    com_name = scrapy.Field()
    invited = scrapy.Field()
    overdue = scrapy.Field()
    def get_intern_position_insert_sql(self):
        # print('进入职位信息')
        insert_sql = """
                    insert into interns_position(
                    position_name,     
                    work_month,
                    maxsal,
                    logo,
                    minsal,
                    city,
                    scale,
                    reslan,
                    attraction,
                    ftype,
                    collected,
                    cuuid,
                    degree,
                    delivered,
                    chance,
                    address,
                    endtime,
                    work_day,
                    work_info,
                    positionUrl,
                    industry,
                    refresh,
                    cname,
                    invited,
                    overdue,
                    created_at
                    )
                    VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') 
                    ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
                """ % (self['positionName'], self['month'], self['maxsal'], self['com_logo'], self['minsal'], self['city'], self['com_scale'], self['reslan'], self['attraction'],
                       self['ftype'],self['collected'], self['cuuid'], self['degree'], self['delivered'], self['chance'], self['work_address'], self['endtime'], self['day'],
                       self['work_info'], self['positionUrl'], self['com_industry'], self['refresh'],self['com_name'], self['invited'], self['overdue'], int(time.time()))
        print(insert_sql)
        return insert_sql

class InternCompanyItem(scrapy.Item):
    #公司信息
    company_info = scrapy.Field()
    reg_num = scrapy.Field()
    scale = scrapy.Field()
    company_name = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    industry = scrapy.Field()
    pranum = scrapy.Field()
    reg_name = scrapy.Field()
    wurl = scrapy.Field()
    is_collect = scrapy.Field()
    cname = scrapy.Field()
    vote_url = scrapy.Field()
    address = scrapy.Field()
    com_url = scrapy.Field()
    logo = scrapy.Field()
    com_type = scrapy.Field()
    reg_capi = scrapy.Field()
    start_time = scrapy.Field()
    types = scrapy.Field()
    description = scrapy.Field()

    def get_intern_company_insert_sql(self):
        # print("进入公司信息")
        insert_sql = """
                       INSERT INTO interns_company(
                       company_info,
                       reg_num,
                       scale,
                       com_name,
                       url,
                       industry,
                       pranum,
                       reg_name,
                       wurl,
                       is_collect,
                       cname,
                       vote_url,
                       address,
                       com_url,
                       logo,
                       com_type,
                       reg_capi,
                       start_time,
                       description,   
                       created_at
                       )
                       VALUES('%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', '%s', '%s',  '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s') 
                       ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
                   """ % (self['company_info'], self['reg_num'], self['scale'], self['company_name'], self['url'], self['industry'],
                            self['pranum'], self['reg_name'],self['wurl'], self['is_collect'], self['cname'], self['vote_url'], self['address'], self['com_url'], self['logo'],
                            self['com_type'], self['reg_capi'],self['start_time'], self['description'], int(time.time()))
        return insert_sql




