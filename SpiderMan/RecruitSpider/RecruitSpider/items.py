# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose , Join
import time
import re

class RecruitspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def RemoveBlankCharacter(value):
    return re.sub(r'\s+', '', value)


def locationDeal(value):
    return value.replace("查看地图","")


def KeyJudge(value):
    return value if value else 'Null'


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
            values(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now()),num=num+1
        """
        params = (self['city'], self['cityInitial'], int(time.time()),1,self['cityTotalNum'])
        return insert_sql, params