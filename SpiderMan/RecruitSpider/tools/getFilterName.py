from sqlalchemy import create_engine


# 获取招聘职位少于15的城市
def getNicheCity():
    sql_str ="select city_name from lagou_city where num <= 15"
    res = sqlExecute(sql_str)
    return res

# 获取已抓取的全部城市
def getAllCatchCity():
    sql_str = "select city_name from lagou_city"
    res = sqlExecute(sql_str)
    return res

def sqlExecute(sql_str):
    engine = create_engine('mysql://root:@localhost:3306/spider?charset=utf8', echo=False)
    conn = engine.connect()
    res = conn.execute(sql_str)
    res_arr = res.fetchall()
    conn.close()
    res_deal = []
    for item in res_arr:
        res_deal.append(item[0])
    return res_deal

if __name__ == "__main__":
    res = getAllCatchCity()
    print(res)