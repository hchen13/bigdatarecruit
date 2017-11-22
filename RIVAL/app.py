import os

from RIVAL import download
from RIVAL import embeddings
from RIVAL.settings import *


def test_font():
	from matplotlib import pylab
	pylab.figure(figsize=(15, 15))
	pylab.scatter(1, 2)
	pylab.annotate('中文', xy=(1, 2))
	pylab.show()

if __name__ == '__main__':
	# download.main()
	files = download.list_save_files()
	embeddings.main(files, save_path=os.path.join(DATA_DIR, 'embeddings.pickle'))
