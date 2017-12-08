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
        select publisher_id,active_time
        from lagou_hr
    '''

    res = database_exec(sql_str)
    return res

# 2、获取51job行业数据
def get51IndustrySql():

    sql = '''
        SELECT industry
        FROM spider.51job_position
    '''

    return sql

def getDatabaseConn():
    engine = create_engine('mysql://{user}:{password}@{host}:3306/{dbname}'.format(**mysql_setting), echo=False)
    conn = engine.connect()
    return conn

# 获取拉钩的职位，和职位标签
def getLagouPositionSql():
    sql = '''
        select position_name, position_labels
        from lagou_recruit_day
    '''
    return sql

# 获取智联的职位和职位标签
def getZhilianPositionSql():
    sql = '''
        select position_name, position_type
        from zhilian_position
    '''
    return sql

# 获取51job的职位和职位标签
def get51jobPositionSql():
    sql = '''
        select name, position_labels
        from 51job_position 
    '''
    return sql
