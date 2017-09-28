from sqlalchemy import create_engine


# 获取招聘职位大于400的城市
def getHotCity():
    sql_str ="select city_name from lagou_city where total_num > 400"
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
    engine = create_engine('mysql://root:Wxk123456@101.200.39.39:3306/spider?charset=utf8', echo=False)
    conn = engine.connect()
    res = conn.execute(sql_str)
    res_arr = res.fetchall()
    conn.close()
    res_deal = []
    for item in res_arr:
        res_deal.append(item[0])
    return res_deal

if __name__ == "__main__":
    res = getSickCity()
    print(res)