import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'RIVAL')

PAGE_SIZE = 1000
MAX_SAVE_FILE_SIZE = 10  # segmented source data file, in MB

LOCAL = False

if LOCAL:
    DB_USER = 'root'
    DB_PASS = 'root'
    DB_HOST = 'localhost'
    DB_NAME = 'spider'
else:
    try:
        DB_USER = os.environ['SPIDER_DB_USER']
        DB_PASS = os.environ['SPIDER_DB_PASS']
        DB_HOST = os.environ['SPIDER_DB_HOST']
        DB_NAME = os.environ['SPIDER_DB_NAME']
    except KeyError as e:
        print("请在环境变量中设置数据库信息: ", e)
        exit()
