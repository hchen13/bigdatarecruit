import os

try:
    DB_USER = os.environ['SPIDER_DB_USER']
    DB_PASS = os.environ['SPIDER_DB_PASS']
    DB_HOST = os.environ['SPIDER_DB_HOST']
    DB_NAME = os.environ['SPIDER_DB_NAME']
except KeyError as e:
    print("请在环境变量中设置数据库信息: ", e)
    exit()