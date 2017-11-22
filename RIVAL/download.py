import sys

import pickle

import re
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from RIVAL import wash
from RIVAL.settings import *

Base = declarative_base()

class LagouJob(Base):
	__tablename__ = 'lagou_recruit_day'
	# __tablename__ = 'test'

	id = Column(Integer, primary_key=True)
	position_name = Column(String)
	position_labels = Column(String)
	first_type = Column(String)
	second_type = Column(String)
	content = Column(String)

	def __repr__(self):
		return self.position_name

	def segment(self):
		words = []
		for k, v in vars(self).items():
			if k.startswith('_') or k == 'id':
				continue
			local_voc = wash.segment(v)
			words += local_voc
		return words

def db_url():
	url_base = '{dialect}+{driver}://{username}:{password}@{host}/{db}?charset=utf8'
	url = url_base.format(
		dialect='mysql', driver='mysqldb',
		username=DB_USER, password=DB_PASS,
		host=DB_HOST, db=DB_NAME
	)
	return url


def connect_database(echo=False):
	print('正在连接数据库...')
	url = db_url()
	engine = create_engine(url, echo=echo)
	Session = sessionmaker(bind=engine)
	print('连接完成\n')
	return engine, Session


def download_batches(target='lagou', page_size=100):
	_, Session = connect_database()
	session = Session()

	try:
		TargetClass = {
			'lagou': LagouJob
		}[target]
	except KeyError as e:
		print('目标Model: {}不存在, 跳过...\n'.format(target))
		return None

	start, stop = 0, page_size
	while True:
		queryset = session.query(TargetClass)
		results = queryset.slice(start, stop).all()
		if results is None or not len(results):
			break
		print('\n成功下载{}条招聘数据'.format(len(results)))
		yield results
		start, stop = stop, stop + page_size


def preprocess_batch(batch):
	print('开始批处理职位信息...')
	words = []
	for position in batch:
		local = position.segment()
		words += local
	print('处理完毕\n')
	print('平均词汇量: {:.2f} 词/职位'.format(len(words)/len(batch)))
	return words


def save(words):

	def get_increment():
		files = list_save_files()
		max_idx = 0
		for file_name in files:
			match = re.search(r'^words(?P<idx>\d+).pickle', file_name)
			idx = int(match.group('idx'))
			max_idx = max(idx + 1, max_idx)
		return max_idx


	print("正在储存词汇, 数量: {}...".format(len(words)))

	idx = get_increment()
	file_name = 'words{}.pickle'.format(idx)
	file_path = os.path.join(DATA_DIR, file_name)
	with open(file_path, 'wb') as fout:
		pickle.dump(words, fout, pickle.HIGHEST_PROTOCOL)
	print('储存完成\n')


def load(file_name):
	if file_name.startswith(DATA_DIR):
		file_path = file_name
	else:
		file_path = os.path.join(DATA_DIR, file_name)
	with open(file_path, 'rb') as fin:
		return pickle.load(fin)


def list_save_files():

	def keyfunc(item):
		match = re.search(r'^words(?P<idx>\d+).pickle', item)
		return int(match.group('idx'))

	file_list = list(filter(is_save_file, os.listdir(DATA_DIR)))
	return sorted(file_list, key=keyfunc)


def is_save_file(file_name):
	result = file_name.startswith('words') and file_name.endswith('.pickle')
	return result


def setup():
	if not os.path.exists(DATA_DIR):
		print("数据储存目录不存在, 创建目录: {}".format(DATA_DIR))
		os.makedirs(DATA_DIR)


def process(batches):
	buff_size = 0
	buff = []
	for batch in batches:
		words = preprocess_batch(batch)
		current_size = sys.getsizeof(words) / 1024 / 1024

		print("Sizes\n\tcurrent batch:\t{:.2f} MB\n\tbuffer:\t\t\t{:.2f} MB\n".format(current_size, buff_size))

		if buff_size + current_size > 10:
			save(buff)
			buff = []
			buff_size = 0
		buff_size += current_size
		buff += words


def main():
	setup()
	targets = ['lagou', 'zhilian', '51job']
	for target in targets:
		batches = download_batches(target=target, page_size=PAGE_SIZE)
		if batches is None:
			continue
		process(batches)


if __name__ == '__main__':
	main()