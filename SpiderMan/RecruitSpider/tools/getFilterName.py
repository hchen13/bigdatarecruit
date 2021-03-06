from sqlalchemy import create_engine
import sys

# 获取招聘职位大于400的城市
def getHotCity():
    sql_str ="select city_name from lagou_city where total_num > 50"
    res = sqlExecute(sql_str)
    return res

# 获取已抓取的全部城市
def getAllCatchCity():
    sql_str = "select city_name from lagou_city"
    res = sqlExecute(sql_str)
    return res

# 获取抓取数据不足的城市
def getSickCity():
    sql_str = "select city_name from lagou_city where total_num > 400 and (num < total_num / 2) order by total_num desc"
    res = sqlExecute(sql_str)
    return res

# 获取已抓取数据的positionID
def getPositionId():
    sql_str = "SELECT position_id FROM spider.lagou_recruit_day"
    res = sqlExecute(sql_str)
    return res

def sqlExecute(sql_str):
    # 判断系统平台, windows平台需加入编码设置
    if 'win32' in sys.platform:
        engine = create_engine('mysql://root:@localhost:3306/spider?charset=utf8', echo=False)
    else:
        engine = create_engine('mysql://root:@localhost:3306/spider?charset=utf8', echo=False)
    conn = engine.connect()
    res = conn.execute(sql_str)
    res_arr = res.fetchall()
    conn.close()
    res_deal = []
    for item in res_arr:
        res_deal.append(item[0])
    return res_deal

# 获取所有城市拼音
def getCityPinYin():
    import pinyin
    sql_str = "select city_name from city where parent_id <> 0 and parent_id <> 2"
    res = sqlExecute(sql_str)
    res_pinyin = []
    for item in res:
        res_pinyin.append(pinyin.get(item, format='strip'))
    return res_pinyin

# 获取智联招聘职位页url
def getZhilianPositionUrlMd5():
    from RecruitSpider.helper import md5
    sql_str = "SELECT url FROM spider.zhilian_position"
    res = sqlExecute(sql_str)
    res_md5 = []
    for item in res:
        res_md5.append(md5(item))
    return res_md5

# 获取爬虫配置
def getConfigureValue(spider_name, key_name):
    sql_str = "SELECT param_value FROM spider.configure where spider = '%s' and param_name = '%s'" % (spider_name, key_name)
    res = sqlExecute(sql_str)
    return res[0]

if __name__ == "__main__":
    res = getConfigureValue('full_city_status')
    print(res)