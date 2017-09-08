# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class RecruitspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LagouItem(scrapy.Item):
    position = scrapy.Field()
    positionID = scrapy.Field()
    positionLables = scrapy.Field()
    salary = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    jobNature = scrapy.Field()
    firstType = scrapy.Field()
    secondType = scrapy.Field()
    city = scrapy.Field()
    distinct = scrapy.Field()

    companyId = scrapy.Field()
    companyFullName = scrapy.Field()
    companyShortName = scrapy.Field()
    companySize = scrapy.Field()
    companyLogo = scrapy.Field()
    industryField = scrapy.Field()
    financeStage = scrapy.Field()

    publisherId = scrapy.Field()
    publishTime = scrapy.Field()
    positionAdavantage = scrapy.Field()
    location = scrapy.Field()
    department = scrapy.Field()
    describe = scrapy.Field()

    hrPortrait = scrapy.Field()
    hrRealName = scrapy.Field()
    hrActiveTime = scrapy.Field()
    hrConnectionLago = scrapy.Field()

