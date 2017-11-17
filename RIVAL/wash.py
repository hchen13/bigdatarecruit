import jieba
import re
from bs4 import BeautifulSoup


def _segment(src):
	if src is None:
		return None
	seg_list = jieba.cut(src, cut_all=False)
	return list(seg_list)


def validate(seg):
	if not len(seg):
		return False

	if seg in ['NULL', ',', '/', ' ', '\n', '.', '，']:
		return False

	if seg in ',.:!@#$%^&*()\，。！、、~`%……‘：；+-=（）':
		return False

	if seg.isdigit():
		return False

	return True


def is_html(src):
	return bool(BeautifulSoup(src, 'html.parser').find())


def strip(src, parser='html'):
	if parser == 'html':

		from html.parser import HTMLParser
		class Stripper(HTMLParser):

			def __init__(self):
				self.reset()
				self.strict = False
				self.convert_charrefs = True
				self.fed = []

			def handle_data(self, d):
				self.fed.append(d)

			def get_data(self):
				return ''.join(self.fed)

		# src = re.sub(r'[^\\xa0-\x7F]+', '', src)
		s = Stripper()
		s.feed(src)
		return s.get_data()


def segment(src=None):
	if is_html(src):
		src = strip(src)
	raw_list = _segment(src)
	seg_list = list(filter(validate, raw_list))
	return seg_list


if __name__ == '__main__':
	pass