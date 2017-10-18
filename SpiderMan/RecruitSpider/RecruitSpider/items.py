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
    return re.sub('人', '', value)


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
