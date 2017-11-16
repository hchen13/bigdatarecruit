from sqlalchemy import create_engine
from settings import *

def database_exec(sql_str):
    engine = create_engine('mysql://{user}:{password}@{host}:3306/{dbname}'.format(**mysql_setting), echo=False)
    conn = engine.connect()
    res = conn.execute(sql_str)
    res_arr = res.fetchall()
    conn.close()
    res_deal = []
    res = []
    for item in res_arr:
        for i in range(len(item)):
            res_deal.append(item[i])
        res.append(res_deal)
        res_deal = []
    return res

# 1、获取hr处理简历的时间
def getLagouHrActiveTime():
    sql_str = '''
        select active_time,count(*) num 
        from lagou_hr 
        where active_time <> 'NULL'and active_time <> '暂无' 
        group by active_time 
        order by num desc
    '''

    res = database_exec(sql_str)
    return res
