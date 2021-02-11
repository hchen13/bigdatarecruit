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
        query_recruit_day = self.dbpool.runInteraction(self.do_insert_recruit_day,item)
        query_city = self.dbpool.runInteraction(self.do_insert_city,item)
        query_hr = self.dbpool.runInteraction(self.do_insert_hr,item)
        query_company = self.dbpool.runInteraction(self.do_insert_company,item)
        # 处理异常
        query_city.addErrback(self.handle_error, item, spider)
        query_company.addErrback(self.handle_error, item, spider)
        query_hr.addErrback(self.handle_error, item, spider)
        query_recruit_day.addErrback(self.handle_error, item, spider)

    def handle_error(self,failure,item,spider):
        print(failure)
        import codecs
        fw = codecs.open('lagou_errLog.txt', 'a', 'utf-8')
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


class ZhilianSpiderPipeline(object):
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
        query_position = self.dbpool.runInteraction(self.do_insert_position,item)
        query_company = self.dbpool.runInteraction(self.do_insert_company,item)
        # 处理异常
        query_position.addErrback(self.handle_error, item, spider)
        query_company.addErrback(self.handle_error, item, spider)

    def handle_error(self,failure,item,spider):
        print(failure)
        import codecs
        fw = codecs.open('zhilian_errLog.txt', 'a', 'utf-8')
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "\r\n" + str(failure))
        fw.close()

    def do_insert_company(self, cursor, item):
        insert_sql, params = item.get_zhilian_company_insert_sql()
        cursor.execute(insert_sql, params)

    def do_insert_position(self, cursor, item):
        insert_sql, params = item.get_zhilian_position_insert_sql()
        cursor.execute(insert_sql, params)


class Job51SpiderPipeline(object):
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
        if 'city_code' in item.keys():
            query_position = self.dbpool.runInteraction(self.do_insert_position,item)
            query_city = self.dbpool.runInteraction(self.do_insert_city, item)
            # 处理异常
            query_position.addErrback(self.handle_error, item, spider)
            query_city.addErrback(self.handle_error, item, spider)

        else:
            query_company = self.dbpool.runInteraction(self.do_insert_company,item)
            # 处理异常
            query_company.addErrback(self.handle_error, item, spider)

    def handle_error(self,failure,item,spider):
        print(failure)
        import codecs
        fw = codecs.open('51job_errLog.txt', 'a', 'utf-8')
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "\r\n" + str(failure))
        fw.close()

    def do_insert_position(self, cursor, item):
        insert_sql, params = item.get_51Job_position_insert_sql()
        cursor.execute(insert_sql, params)

    def do_insert_city(self, cursor, item):
        insert_sql, params = item.get_51Job_city_insert_sql()
        cursor.execute(insert_sql, params)

    def do_insert_company(self, cursor, item):
        insert_sql, params = item.get_51Job_company_insert_sql()
        cursor.execute(insert_sql, params)

class BossSpiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    # 存取Boss直聘的所有城市及其编码
    def do_insert_findCity(self, cursor, item):
        insert_sql = item.get_findCity_insert_sql()
        cursor.execute(insert_sql)

    # 获取职位类型
    def do_insert_positionType(self, cursor, item):
        insert_sql = item.get_findPositionType_insert_sql
        cursor.execute(insert_sql)

    def do_insert_company(self, cursor, item):
        insert_sql = item.get_boss_company_insert_sql()
        cursor.execute(insert_sql)

    def do_insert_position(self, cursor, item):
        insert_sql = item.get_boss_position_insert_sql()
        print(insert_sql)
        cursor.execute(insert_sql)

    def process_item(self, item, spider):
        # 异步插入
        # query_findCity = self.dbpool.runInteraction(self.do_insert_findCity, item)
        # query_positionType = self.dbpool.runInteraction(self.do_insert_positionType, item)
        query_position = self.dbpool.runInteraction(self.do_insert_position, item)
        query_company = self.dbpool.runInteraction(self.do_insert_company, item)

        # 处理异常
        # query_positionType.addErrback(self.handle_error, item, spider)
        # query_findCity.addErrback(self.handle_error, item, spider)
        query_position.addErrback(self.handle_error, item, spider)
        query_company.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)
        import codecs
        fw = codecs.open('boss_errLog.txt', 'a', 'utf-8')
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\r\n" + str(failure))
        fw.close()

class InternsSpiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

        # 存取实习僧的所有城市及其编码
    def do_insert_findIntensCity(self, cursor, item):
        insert_sql = item.get_findInternsCity_insert_sql()
        cursor.execute(insert_sql)

    def process_item(self, item, spider):
        # 异步插入
        # query_findInternsCity = self.dbpool.runInteraction(self.do_insert_findIntensCity, item)
        query = self.dbpool.runInteraction(self.do_insert_intern , item)
        # 处理异常
        # query_findInternsCity.addErrback(self.handle_error, item, spider)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print(failure)

        import codecs
        fw = codecs.open('interns_errLog.txt', 'a', 'utf-8')
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\r\n" + str(failure))
        fw.close()

    def do_insert_intern(self, cursor, item):
        if len(item) == 25:
            insert_sql = item.get_intern_position_insert_sql()
            cursor.execute(insert_sql)
        else:
            insert_sql = item.get_intern_company_insert_sql()
            return cursor.execute(insert_sql)

class stateSpiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)


    def do_update_position(self, cursor, item):
        url = item['url']
        if 'lagou' in url:
            update_sql = item.get_recruit_day_update_sql()
            cursor.execute(update_sql)
        elif 'jobs.zhaopin.com' in url:
            update_sql = item.get_zhilian_position_update_sql()
            cursor.execute(update_sql)
        elif '51job' in url and len(item) == 3:
            update_sql = item.get_51Job_position_update_sql()
            cursor.execute(update_sql)
        elif len(item) == 4:
            update_sql = item.get_51Job2017_position_update_sql()
            cursor.execute(update_sql)

    def process_item(self, item, spider):
        # 异步插入
        query = self.dbpool.runInteraction(self.do_update_position, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print(failure)
        import codecs
        fw = codecs.open('state_errLog.txt', 'a', 'utf-8')
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\r\n" + str(failure))
        fw.close()