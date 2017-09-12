# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose , Join
import time


class RecruitspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def RemoveBlankCharacter(value):
    return value.replace("\r","").replace("\t","").replace("\n","").replace(" ","")


def locationDeal(value):
    return value.replace("查看地图","")


def KeyJudge(value):
    return value if value else 'Null'


class LagouItem(scrapy.Item):

    cityInitial = scrapy.Field()
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
        financeStage = vars().get("self['financeStage']", 'NULL')
        industryField = vars().get("self['industryField']", 'NULL')
        companySize = vars().get("self['companySize']", 'NULL')
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
        params = (self['companyId'], self['companyFullName'], self['companyShortName'], companySize,self['companyLogo'],industryField,financeStage,int(time.time()),1)
        return insert_sql,params

    def get_hr_insert_sql(self):
        hrActiveTime = vars().get("self['hrActiveTime']",'NULL')
        hrPositionName = vars().get("self['hrPositionName']",'NULL')
        hrPortrait = vars().get("self['hrPortrait']",'NULL')

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
        params = (self['publisherId'], hrPositionName, hrPortrait, self['hrRealName'], self['positionId'],hrActiveTime, self['hrConnectionLagou'], int(time.time()),1)
        return insert_sql, params

    def get_recruit_day_insert_sql(self):

        positionLabels = vars().get("self['positionLabels']",'NULL')
        district = vars().get("self['district']", 'NULL')

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
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now())
        """
        params = (self['positionId'], self['url'] , self['positionName'], positionLabels, self['salary'], self['workYear'], self['education'], self['jobNature'], self['firstType'], self['secondType'],self['city'], district, self['companyId'], self['positionAdvantage'], self['location'], self['publisherId'], self['publishTime'], self['department'], self['describe'], int(time.time()))
        return insert_sql, params

    def get_city_insert_sql(self):
        import time

        insert_sql = """
            insert into lagou_city(
            city_name,
            name_initial,
            created_at,
            num
            ) 
            values(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE created_at=unix_timestamp(now()),num=num+1
        """
        params = (self['city'], self['cityInitial'], int(time.time()),1)
        return insert_sql, params