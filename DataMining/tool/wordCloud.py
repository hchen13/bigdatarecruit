import jieba
import re
from wordcloud import WordCloud
from scipy.misc import imread
import matplotlib.pyplot as plt
import codecs
import jieba.posseg as pseg
# Read the whole text.
# @params content 具体内容 (依据type分别传入文字，地址，sql语句)
# @params type 1、文字 2、文件
# @params status 1、开启分词 2、关闭分词
# @params temple_pic_path 样本图片路径
# @params pic_file_path 输出图片路径
# @params font_path 字体路径
def getWordCloud(content='', type = 1, status = 1, temple_pic_path = './cloud.jpeg' ,pic_file_path = './examples.jpg', font_path='/System/Library/Fonts/STHeiti Light.ttc'):

    remove_word_compile = r'我们|其他|要求|具有|编写|完成|项目|以上|以及|常用|根据|参与|考虑|开发|技术|熟悉|熟练|产品|经验|公司|相关|优先|工作|具备|了解|需求|任职|职位|职能|使用|类别|进行|岗位职责|掌握|或者|负责|良好|地址'

    if type == 1:
        words = content
    elif type == 2:
        with codecs.open(content) as f:
            words = f.read()
    # 需要去掉的字符
    del_list_compile = re.compile(r"[，|。|、|\n|”|“|的|和|<.*?>]")
    word_deal = re.sub(remove_word_compile,' ', re.sub(del_list_compile, ' ', re.sub(r'<.*?>', '', words)))
    if status == 1:
        str_list = jieba.cut(word_deal, cut_all=False)
        words = ' '.join(str_list)

    color_mask = imread(temple_pic_path)

    wordcloud = WordCloud(font_path=font_path, max_font_size=80, background_color='white', mask=color_mask).generate(words)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # plt.show()
    plt.savefig(pic_file_path)