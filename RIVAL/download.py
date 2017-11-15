from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from RIVAL.settings import *


Base = declarative_base()
Session = sessionmaker()

def db_url():
	url_base = '{dialect}+{driver}://{username}:{password}@{host}/{db}?charset=utf8'
	url = url_base.format(
		dialect='mysql', driver='mysqldb',
		username=DB_USER, password=DB_PASS,
		host=DB_HOST, db=DB_NAME
	)
	return url


def init_database(echo=False):
	print('正在初始化数据库...')
	url = db_url()
	engine = create_engine(url, echo=echo)



if __name__ == '__main__':
	pass