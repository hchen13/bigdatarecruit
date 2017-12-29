from tool.database import getDatabaseConn, getJ5Advantage, getLGPositionContent
from tool.wordCloud import getWordCloud
import pandas as pd

# 获取51job职位诱惑词云
def getJ5PositionWordCloud():
    res_df = pd.read_sql(getJ5Advantage(), getDatabaseConn())
    words = ' '.join(res_df.advantage)
    getWordCloud(content=words, type=1, status=2)

# 获取it行业职位描述词云
def getLagouPositionWordCloud(query_name):
    res_df = pd.read_sql(getLGPositionContent(), getDatabaseConn())
    res_df = res_df[res_df['position_name'].str.contains(query_name)]
    words = ' '.join(res_df.content)
    getWordCloud(content=words, type=1, status=1, pic_file_path='./python.jpg')