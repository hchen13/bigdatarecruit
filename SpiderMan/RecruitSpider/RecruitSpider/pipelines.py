# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import time

class RecruitSpiderPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            db = settings['MYSQL_DBNAME'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 异步插入
        query_city = self.dbpool.runInteraction(self.do_insert_city,item)
        query_hr = self.dbpool.runInteraction(self.do_insert_hr,item)
        query_company = self.dbpool.runInteraction(self.do_insert_company,item)
        query_recruit_day = self.dbpool.runInteraction(self.do_insert_recruit_day,item)
        # 处理异常
        query_city.addErrback(self.handle_error, item, spider)
        query_company.addErrback(self.handle_error, item, spider)
        query_hr.addErrback(self.handle_error, item, spider)
        query_recruit_day.addErrback(self.handle_error, item, spider)

    def handle_error(self,failure,item,spider):
        print(failure)
        import codecs
        fw = codecs.open('errLog.txt', 'a', 'utf-8')
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "\r\n" + str(failure))
        fw.close()

    def do_insert_city(self, cursor, item):
        insert_sql, params = item.get_city_insert_sql()
        cursor.execute(insert_sql, params)

    def do_insert_hr(self, cursor,item):
        insert_sql, params = item.get_hr_insert_sql()
        cursor.execute(insert_sql, params)

    def do_insert_company(self ,cursor, item):
        insert_sql, params = item.get_company_insert_sql()
        cursor.execute(insert_sql, params)

    def do_insert_recruit_day(self, cursor, item):
        insert_sql, params = item.get_recruit_day_insert_sql()
        cursor.execute(insert_sql, params)
