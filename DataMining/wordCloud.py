from tool.database import getDatabaseConn, getJ5Advantage, getLGPositionContent, getZLPositionContent, getJ5PositionContent
from tool.wordCloud import getWordCloud
import pandas as pd
import os
import re
# 获取51job职位诱惑词云
def getJ5PositionWordCloud():
    res_df = pd.read_sql(getJ5Advantage(), getDatabaseConn())
    words = ' '.join(res_df.advantage)
    getWordCloud(content=words, type=1, status=2)

# 获取it行业职位描述词云
# @param query_name 查询职位名称
# @param type 1、lagou 2、智联 3、51
# @param db_type 1、读取数据库 2、读取缓存文件
def getLagouPositionWordCloud(query_name, type=1, db_type=1):

    if db_type == 1:
        if type == 1:
            sql = getLGPositionContent()
        elif type == 2:
            sql = getZLPositionContent()
        elif type == 3:
            sql = getJ5PositionContent()

        res_df = pd.read_sql(sql, getDatabaseConn())
        res_df.to_hdf('/Users/monstar/Desktop/lg_wc.h5', 'wordCloud')
    else:
        res_df = pd.read_hdf('/Users/monstar/Desktop/lg_wc.h5')
    res_df = res_df[res_df['position_name'].str.contains(re.escape(query_name))]
    words = ' '.join(res_df.content)
    getWordCloud(content=words, type=1, status=1, pic_file_path= os.path.join('/Users/monstar/Desktop', query_name + '.jpg'))