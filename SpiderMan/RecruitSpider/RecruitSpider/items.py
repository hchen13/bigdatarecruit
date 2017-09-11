# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose , Join


class RecruitspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LagouItem(scrapy.Item):
    position = scrapy.Field()
    positionID = scrapy.Field()
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
        output_processor=Join(",")
    )
    department = scrapy.Field()
    describe = scrapy.Field()

    hrPortrait = scrapy.Field()
    hrRealName = scrapy.Field()
    hrActiveTime = scrapy.Field()
    hrConnectionLago = scrapy.Field()
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
            finance_stage
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """
        params = ()
        return insert_sql

    def get_hr_insert_sql(self):
        insert_sql = """
            insert into lagou_company(
            company_id,
            full_name,
            short_name,
            size,
            logo,
            industry,
            finance_stage
            ) 
            values(%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """
        pass

    def get_recruit_day_insert_sql(self):
        insert_sql = """
            insert into lagou_company(
            position_id,
            position_name,
            position_labels,

            ) 
            values() ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """
        pass

