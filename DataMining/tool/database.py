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

# 只获取51job的职位标签
def get51jobPositionLabels():
    sql = '''
        select position_labels
        from 51job_position where position_labels <> '其他'
    '''
    return sql

# 获取51标签为其他的职位名称
def get51jobOtherName():
    sql = '''
        select name as position_labels from 51job_position where position_labels = '其他'
    '''
    return sql

# 获取智联的职位标签
def getZhilianPositionType():
    sql = '''
        select position_type from zhilian_position where position_type <> '其他'
    '''
    return sql

# 获取智联的职位
def getZhilianPositionName():
    sql = '''
        select position_name as position_type from zhilian_position where position_type = '其他'
    '''
    return sql

# 获取拉钩的的第二分类
def getLagouSecondtype():
    sql = '''
        select second_type from lagou_recruit_day where second_type <> 'NULL'
    '''
    return sql

# 获取拉钩hr的信息
def getLagouHrInfo():
    sql = '''
        select publisher_id,real_name,num as self_num from lagou_hr
    '''
    return sql

# 获取拉钩hr_id和公司id
def getLagourHrComId():
    sql = '''
        select publisher_id, company_id from lagou_recruit_day group by publisher_id, company_id
    '''
    return sql

# 获取拉钩公司信息
def getLagouCompanyInfo():
    sql = '''
        select company_id, full_name, short_name, size, industry, finance_stage, num as total_num from lagou_company
    '''
    return sql

# 获取智联职位信息
def getZhilianPositionSql():
    sql = '''
        select company_md5, position_name, salary_low, salary_high, work_year, education, recruit_num from zhilian_position
    '''
    return sql

# 获取51job职位信息
def get51JobPositionSql():
    sql = '''
        select company_md5, name, salary, education, recruit_num from 51job_position
    '''
    return sql

# 获取智联公司信息
def getZhilianCompanySql():
    sql = '''
        select 
            company_md5, full_name, size, company_nature, industry
        from zhilian_company
    '''
    return sql

# 获取51job公司信息
def get51JobCompanySql():
    sql = '''
        select 
            company_md5, full_name, size, company_nature, industry
        from 51job_company
    '''
    return sql

# 获取智联薪水年限和教育程度
def getZhilianZCSql():
    sql = '''
        select salary_low, salary_high, work_year, education from zhilian_position
    '''
    return sql

# 获取51薪水年限和教育程度
def getJ5ZCSql():
    sql = '''
        select salary, work_year, education, city, industry from 51job_position
    '''
    return sql

# 获取拉钩职位标签，名称，年限，教育程度，薪水
def getLagouPositionInfo():
    sql = '''
        select position_name, position_labels, salary, work_year, education, second_type, city
        from lagou_recruit_day
    '''
    return sql

# 智联 具体职位薪资排行
def getZLSalaryByPositionSql():
    sql = '''
        select city, salary_low, salary_high, work_year, education, position_type from zhilian_position
    '''
    return sql