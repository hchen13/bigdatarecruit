import jieba
import re
from wordcloud import WordCloud
from scipy.misc import imread
import matplotlib.pyplot as plt
import codecs

# Read the whole text.
with codecs.open('/Users/monstar/Desktop/ProjectCode/personal/test/py3env/jk.txt', encoding='gbk') as f:
    str_article = f.read()
del_list_compile = re.compile(r"[，|。|、|\n|”|“|的|和]")
str_list = jieba.cut(re.sub(del_list_compile, '', str_article), cut_all=True)
text = ' '.join(str_list)
color_mask = imread("/Users/monstar/Documents/picture/cloud.jpeg")

wordcloud = WordCloud(font_path='/System/Library/Fonts/STHeiti Light.ttc', max_font_size=80, background_color='white', mask=color_mask).generate(str_article)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
plt.savefig("./examples.jpg")