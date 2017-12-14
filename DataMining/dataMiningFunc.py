from tool import database, helper
import pandas as pd
import numpy as np

# ******************************** hr排行 *************************************
# 获取公司hr数量排行
# @return DataFrame
def lagouCompanyHrRankDf():
    # 获取数据库连接和sql
    conn = database.getDatabaseConn()
    sql_lagou_hr = database.getLagouHrInfo()
    sql_lagou_recruit_day = database.getLagourHrComId()
    sql_lagou_company = database.getLagouCompanyInfo()
    # 读取数据
    lagou_hr_df = pd.read_sql(sql_lagou_hr, conn)
    lagou_recruit_day = pd.read_sql(sql_lagou_recruit_day, conn)
    lagou_company = pd.read_sql(sql_lagou_company, conn)
    # 连接三张表，首先获取公司hr数量
    res_lrd_df = pd.merge(lagou_recruit_day, lagou_hr_df, on='publisher_id', how='left')
    res_com_df = pd.merge(lagou_company, res_lrd_df, on='company_id', how='left')
    res_com_df = res_com_df.set_index('company_id')
    res_g = res_com_df.groupby(['company_id'])
    res_hr_num_df = res_g.size().to_frame().rename(columns={0: 'hr_num'})
    # 然后将数量信息和公司表连接
    company_hr_num_df = pd.concat([lagou_company.set_index('company_id'), res_hr_num_df], axis=1)
    res = company_hr_num_df.sort_values('hr_num', ascending=False)
    return res

# 统计拉钩公司hr数量排行
def lagouCompanyHrNum():
    df = lagouCompanyHrRankDf()
    res = pd.DataFrame(df.set_index('short_name'), columns=['hr_num']).sort_values('hr_num', ascending=False)
    return res

# 统计拉钩hr数量在前100的公司规模占比
def lagouCompanySizeByHrNum():
    df = lagouCompanyHrRankDf()[:100]
    res = df.groupby('size').size().sort_values(ascending=False).to_json(orient='index', force_ascii=False)
    return res

# 统计拉钩hr数量在前100的公司类型占比
def lagouCompanySizeByHrNum():
    df = lagouCompanyHrRankDf()[:100]
    res = df.groupby('finance_stage').size().sort_values(ascending=False).to_json(orient='index', force_ascii=False)
    return res

# 统计拉钩招聘数量在前100的公司
def lagouCompanyPositionNum():
    df = lagouCompanyHrRankDf()
    res = df.sort_values('total_num', ascending=False)[:100].to_json(orient='index', force_ascii=False)
    return res

# 统计hr各时段处理简历的数量
def hrRecruitTime():
    res = database.getLagouHrActiveTime()
    d = pd.DataFrame(res, columns = ['id', 'time'])
    data = d[d.time != '暂无']
    res = data.groupby('time').size().sort_values()
    return res.to_json(orient='index', force_ascii=False)

# 统计51job各行业职位数辆 前60
def get51IndustryNum():
    # 获取行业数据
    sql = database.get51IndustrySql()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    data = pd.read_sql(sql, conn)
    data = data[(True ^ data.industry.isin(['1000-5000人', '5000-10000人', '500-1000人', '少于50人', '150-500人', '50-150人']))]
    data_sort = data.groupby('industry').size().sort_values(ascending=False)[:60]
    return data_sort.to_json(orient='index', force_ascii=False)

####################################### 编程语言排行 ################################################################

# 通过关键字查找数量
# @params df 要查找的DataFrame数据集
# @params query_key 要查找的字段
# @params query_list 要查找的字符串
# @return DataFrame
def getNumByKeyWords(df, query_key, query_list):
    query_rank = {}
    for item in query_list:
        name = item.replace("\\", '')
        name = 'objective-c' if name == 'ios' else name
        num = 0
        for value in query_key:
            num += df[df[value].str.contains(item)].size
        query_rank[name] = num
    query_series = pd.Series(query_rank)
    res = pd.DataFrame([query_series], index=['数量']).T.sort_values(['数量'])
    return res

# 编程语言排行
# @param sql 查询sql
# @param query_key 查询字段
# @return
def programingPositionRank(sql, query_key):
    # 获取数据库连接
    conn = database.getDatabaseConn()
    # 获取常用语言
    programing_language_list = helper.getProgramingLanguage()
    # 获取数据
    lg_rd_df = pd.read_sql(sql, conn)
    conn.close()
    # 查询数据
    lg_df_programing_rank = getNumByKeyWords(lg_rd_df, query_key, programing_language_list)
    return lg_df_programing_rank

# 统计拉钩招聘职位中编程语言排行
def lagouRecruitCodeRank():
    # 获取拉钩的sql
    sql = database.getLagouPositionSql()
    query_key = ['position_name', 'position_labels']
    res = programingPositionRank(sql, query_key)
    return res.to_json(orient='index', force_ascii=False)

# 获取智联招聘编程语言排行
def zhilianPositionCodeRank():
    # 获取智联的sql
    sql = database.getZhilianPositionSql()
    query_key = ['position_name', 'position_type']
    res = programingPositionRank(sql, query_key)
    return res.to_json(orient='index', force_ascii=False)

# 获取51job编程语言职位排行
def job51PositionCodeRank():
    # 获取51job的sql
    sql = database.get51jobPositionSql()
    query_key = ['name', 'position_labels']
    res = programingPositionRank(sql, query_key)
    return res.to_json(orient='index', force_ascii=False)

# ***********************************  获取职位排行  *********************************
# @param df DataFrame
def getPositionRank(df, column_name):
    res_list = ','.join(df[column_name]).split(',')
    res_def = pd.DataFrame(res_list, index=np.arange(len(res_list)))
    res_def = res_def.rename(columns={0: 'position_labels'})
    res_group = res_def.groupby('position_labels')
    # 销售岗
    sale_total_num = res_group.size()[False ^ res_group.size().index.str.contains('销售|客户代表')].sum()
    # 教师
    teacher_total_num = res_group.size()[False ^ res_group.size().index.str.contains('教师|老师')].sum()
    # 人事
    renshi_total_num = res_group.size()[False ^ res_group.size().index.str.contains('人事')].sum()
    # 前端
    frontend_total_num = res_group.size()[False ^ res_group.size().index.str.contains('前端')].sum()

    res_choose = res_group.size()[True ^ res_group.size().index.str.contains(
        '教师|老师|销售|客户代表|五险一金|节日福利|双休|立即上岗|应届生|员工旅游|交通补助|培训|出差补贴|话补|加班补助|全勤奖|人事|带薪年假|前端开发')]
    res_choose['销售'] = sale_total_num
    res_choose['教师'] = teacher_total_num
    res_choose['人事'] = renshi_total_num
    res_choose['前端开发'] = frontend_total_num
    return res_choose

# 获取51job全国招聘职位数排行 前60
def job51PositionRank():
    # 获取51job的sql
    sql = database.get51jobPositionLabels()
    sql_Other = database.get51jobOtherName()
    # 获取数据库连接
    conn = database.getDatabaseConn()

    position_res_df = pd.concat([pd.read_sql(sql, conn), pd.read_sql(sql_Other, conn)])

    res_choose = getPositionRank(position_res_df, 'position_labels')

    return res_choose.sort_values(ascending=False)[0:60].to_json(orient='index', force_ascii=False)

# 获取智联全国招聘职位数排行 前60
def zhilianPositionRank():
    # 获取51job的sql
    sql = database.getZhilianPositionType()
    sql_Other = database.getZhilianPositionName()
    # 获取数据库连接
    conn = database.getDatabaseConn()

    position_res_df = pd.concat([pd.read_sql(sql, conn), pd.read_sql(sql_Other, conn)])

    res_choose = getPositionRank(position_res_df, 'position_type')

    return res_choose.sort_values(ascending=False)[0:60].to_json(orient='index', force_ascii=False)

# 获取拉钩全国招聘职位数排行 前60 （it行业招聘职位排行）
def lagouPositionRank():
    # 获取51job的sql
    sql = database.getLagouSecondtype()
    # 获取数据库连接
    conn = database.getDatabaseConn()

    position_res_df = pd.read_sql(sql, conn)

    res_choose = getPositionRank(position_res_df, 'second_type')

    return res_choose.sort_values(ascending=False)[0:60].to_json(orient='index', force_ascii=False)

# *********************************  公司招聘职位数排行  ********************************
# 智联公司招聘职位数
def zhilianCompanyPositionNum():
    # 获取51job的sql
    sql_position = database.getZhilianPositionSql()
    sql_company = database.getZhilianCompanySql()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    zp_df = pd.read_sql(sql_position, conn)
    zc_df = pd.read_sql(sql_company, conn)
    res_zp = pd.merge(zp_df, zc_df, on='company_md5', how='left')
    res_zp_g = res_zp.groupby('full_name').size().sort_values(ascending=False)
    return res_zp_g[0:60].to_json(orient='index', force_ascii=False)

# 智联招聘职位前100里，公司规模占比
# @param type 1 规模 2 企业性质 3 行业
def zhilianCompanyHighNumType(type=1):
    # 获取51job的sql
    sql_position = database.getZhilianPositionSql()
    sql_company = database.getZhilianCompanySql()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    zp_df = pd.read_sql(sql_position, conn)
    zc_df = pd.read_sql(sql_company, conn)
    res_zp = pd.merge(zp_df, zc_df, on='company_md5', how='left')
    res_zp_g = res_zp.groupby('full_name').size()
    res_zp_g = pd.DataFrame(list(zip(res_zp_g.index, res_zp_g.values))).rename(
        columns={0: 'full_name', 1: "total_recruit_num"})
    res_total = pd.merge(zc_df, res_zp_g, on='full_name', how='left').sort_values('total_recruit_num',
                                                                                   ascending=False)[:100]
    if type == 1:
        query_column = 'size'
    elif type == 2:
        query_column = 'company_nature'
    elif type == 3:
        query_column = 'industry'
    res = res_total.groupby(query_column).size().sort_values(ascending=False)
    return res.to_json(orient='index', force_ascii=False)

# 51公司招聘职位数
def job51CompanyPositionNum():
    # 获取51job的sql
    sql_position = database.get51JobPositionSql()
    sql_company = database.get51JobCompanySql()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    j5_df = pd.read_sql(sql_position, conn)
    j5c_df = pd.read_sql(sql_company, conn)
    res_j5 = pd.merge(j5_df, j5c_df, on='company_md5', how='left')
    res_j5_g = res_j5.groupby('full_name').size().sort_values(ascending=False)
    return res_j5_g[0:60].to_json(orient='index', force_ascii=False)

# 51job招聘职位前100里，公司规模占比
# @param type 1 规模 2 企业性质 3 行业
def job51CompanyHighNumType(type=1):
    # 获取51job的sql
    sql_position = database.get51JobPositionSql()
    sql_company = database.get51JobCompanySql()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    j5_df = pd.read_sql(sql_position, conn)
    j5c_df = pd.read_sql(sql_company, conn)
    res_j5 = pd.merge(j5_df, j5c_df, on='company_md5', how='left')
    res_j5_g = res_j5.groupby('full_name').size()
    res_j5_g = pd.DataFrame(list(zip(res_j5_g.index, res_j5_g.values))).rename(
        columns={0: 'full_name', 1: "total_recruit_num"})
    res_total = pd.merge(j5c_df, res_j5_g, on='full_name', how='left').sort_values('total_recruit_num',
                                                                                   ascending=False)[:100]
    if type == 1:
        query_column = 'size'
    elif type == 2:
        query_column = 'company_nature'
    elif type == 3:
        query_column = 'industry'
    res = res_total.groupby(query_column).size().sort_values(ascending=False)
    return res.to_json(orient='index', force_ascii=False)

# 获取工作年限数统计
# @param sql 统计字段work_year
# @return Series
def workYearNum(sql):
    # 获取数据库连接
    conn = database.getDatabaseConn()
    df = pd.read_sql(sql, conn)
    df_g = df.groupby('work_year')
    return df_g.size().sort_values(ascending=False)[:7]

# 智联工作年限招聘数
def zhilianWorkYearNum():
    sql = database.getZhilianZCSql()
    res_series = workYearNum(sql)
    return res_series.to_json(orient='index', force_ascii=False)

# 51工作年限招聘数
def j5WorkYearNum():
    sql = database.getJ5ZCSql()
    res_series = workYearNum(sql)
    return res_series.to_json(orient='index', force_ascii=False)

# 拉钩工作年限招聘数
def lagouWorkYearNum():
    sql = database.getLagouPositionInfo()
    res_series = workYearNum(sql)
    return res_series.to_json(orient='index', force_ascii=False)

def salarySplit(line):
    import re
    res = re.match(r'([\d]+)K-([\d]+)K', line)
    if not res:
        res = re.match(r'([\d]+)k-([\d]+)k', line)
    if res:
        salary_low = res[1]
        salary_high = res[2]
        salary_mean = (int(salary_low) + int(salary_high)) / 2
    else:
        res = re.match(r'([\d]+).*', line)
        salary_low = res[1]
        salary_high = res[1]
        salary_mean = res[1]
    return pd.Series([salary_low, salary_high, salary_mean])

# 拉钩薪资分布
def lagouSalaryDistribution():
    sql = database.getLagouPositionInfo()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    df = pd.read_sql(sql, conn)
    tmp = df['salary'].apply(salarySplit).rename(columns={0:'salary_low', 1:'salary_high', 2:'salary_mean'})
    df = df.combine_first(tmp).to_json(orient='index', force_ascii=False)
    df_filter = pd.DataFrame([])