from tool import database, helper
import pandas as pd
import numpy as np
import json

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
    # 获取拉钩的sql
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

# 拉钩薪资整体情况
# @return DataFrame 包含最高、最低、平均工资的招聘职位信息
def lagouSalaryDetail():
    sql = database.getLagouPositionInfo()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    df = pd.read_sql(sql, conn)
    tmp = df['salary'].apply(salarySplit).rename(columns={0:'salary_low', 1:'salary_high', 2:'salary_mean'})
    df = df.combine_first(tmp)
    return df

# 拉钩整体平均薪资情况(中位数)
def lagouWholeSalaryDistribution():
    df = lagouSalaryDetail()
    df_filter = pd.DataFrame(df, columns=['salary_high', 'salary_low', 'salary_mean'])
    return df_filter.salary_mean.describe()['50%']

# 拉钩个工作年限薪资情况
# @param type 1, 50% 中位数 2，std 标准差
# @return json
def lagouWorkYearSalary(type = 1):
    df = lagouSalaryDetail()
    df_work_res = df[df.work_year != '1-3'].groupby('work_year').salary_mean.describe().sort_values(['50%'],ascending=False)
    if type == 1:
        res = df_work_res['50%'].apply(lambda x: round(x, 2))
    elif type == 2:
        res = df_work_res['std'].apply(lambda x: round(x, 2))
    return res.to_json(orient='index', force_ascii=False)

# 51job网站薪资处理函数
def job51SalaryDeal(line):
    import re
    patten1 = r'([\d]+.?[\d]?)-([\d]+.?[\d]?)千/月'
    patten2 = r'([\d]+.?[\d]?)-([\d]+.?[\d]?)万/月'
    patten3 = r'([\d]+.?[\d]?)-([\d]+.?[\d]?)万/年'
    low = high = mean = 0
    if re.compile(patten1).match(line):
        low = float(re.compile(patten1).match(line).group(1))
        high = float(re.compile(patten1).match(line).group(2))
        mean = int((low + high)) / 2
    elif re.compile(patten2).match(line):
        low = float(re.compile(patten2).match(line).group(1)) * 10
        high = float(re.compile(patten2).match(line).group(2)) * 10
        mean = int((low + high)) / 2
    elif re.compile(patten3).match(line):
        low = float(re.compile(patten3).match(line).group(1)) * 10 / 12
        high = float(re.compile(patten3).match(line).group(2)) * 10 / 12
        mean = int(low + high) / 2
    return pd.Series([round(low, 2), round(high, 2), round(mean, 2)])

# 51job薪资情况
# 获取51job工作年限，教育水平，薪资 （此方法运行时间将近15分钟）
# @param type 1、默认使用以生成好的h5文件 2、重新生成
def job51SalaryPosition(type=1):
    import os
    # 获取数据库连接
    if type == 1 & os.path.exists('./salaryWE.h5'):
        df_res = pd.read_hdf('./salaryWE.h5')
    else:
        conn = database.getDatabaseConn()
        sql = database.getJ5ZCSql()
        df_51job_salary = pd.read_sql(sql, conn)
        df_51job_salary = df_51job_salary[df_51job_salary.salary != 'NULL']
        df_51job_salary_deal = df_51job_salary[True ^ df_51job_salary['salary'].str.contains('天|小时|\+')]
        df_tmp = df_51job_salary_deal.salary.apply(job51SalaryDeal)
        df_res = df_51job_salary_deal.combine_first(df_tmp.rename(columns={0: 'low', 1: 'high', 2: 'mean'}))
        df_res.to_hdf('./salaryWE.h5', 'salary_all')
    return df_res

# 返回标准函数
def resDeal(df_res):
    res_dict = {}
    df = df_res[df_res.index != 'NULL']
    res_mean_dict = df['mean'].to_dict()
    res_std_dict = df['std'].to_dict()
    res_count_dict = df['count'].to_dict()
    res_dict['key_name'] = list(res_mean_dict.keys())
    res_dict['count'] = list(res_count_dict.values())
    res_dict['salary'] = list(map(lambda x: int(x * 1000), res_mean_dict.values()))
    res_dict['std'] = list(map(lambda x: round(x + 20, 2), res_std_dict.values()))
    return json.dumps(res_dict)

# 获取51job整体薪资中位数
# @param type 1、从h5结果获取数据 2、重新生成数据
def get51jobSalaryMiddle(type=1):
    df = job51SalaryPosition(type)
    return df.describe().apply(lambda x: round(x * 1000, 2))['mean']['mean']

# 获取51job教育程度招聘数情况
def get51jobRecruitNumByEducation():
    # 获取数据库连接
    conn = database.getDatabaseConn()
    sql = database.getJ5ZCSql()
    df_51job_salary = pd.read_sql(sql, conn)
    return df_51job_salary.groupby('education').size().sort_values(ascending=False).to_json(orient='index', force_ascii=False)

# 获取51job教育程度与薪资关系
def get51jobSalaryByEducation():
    df = job51SalaryPosition()
    df_res = df.groupby('education')['mean'].describe().sort_values(['mean'], ascending=False)
    return resDeal(df_res)

# 51job工作年限与薪资关系
def get51jobSalaryByWorkYear():
    df = job51SalaryPosition()
    df_res = df.groupby('work_year')['mean'].describe().sort_values(['mean'])
    return resDeal(df_res)

# 51job根据教育水平和工作年限分析薪资情况
def get51jobSalaryByWE():
    df = job51SalaryPosition()
    df_rename = df.rename(columns={'work_year' : '工作年限', 'mean' : '平均薪资', 'education' : '教育程度'})
    df_res = df_rename.pivot_table(index=['工作年限'], columns='教育程度', values=['平均薪资']).rename(columns={'NULL' : '其他'}).apply(lambda x: round(x * 1000,0))
    return df_res.T.to_json(orient='split', force_ascii=False)

# 51job行业薪资情况
# @return 行业名称 平均薪资 标准差
def get51jobSalaryByIndustry():
    df = job51SalaryPosition()
    df = df[(True ^ df.industry.isin(['1000-5000人', '5000-10000人', '500-1000人', '少于50人', '150-500人', '50-150人']))]
    df_res = df.groupby('industry')['mean'].describe()
    df_j5_industry_salary = df_res[df_res['count'] > 10].sort_values('mean', ascending=False).apply(
        lambda x: round(x, 2))
    res_mean = df_j5_industry_salary['mean'].to_dict()
    res_std = df_j5_industry_salary['std'].to_dict()
    return list(res_mean.keys()), list(map(lambda x: int(x * 1000), res_mean.values())), list(res_std.values())

# 51job行业薪资标准差情况
def get51jobSalaryStdByIndustry():
    df = job51SalaryPosition()
    df = df[(True ^ df.industry.isin(['1000-5000人', '5000-10000人', '500-1000人', '少于50人', '150-500人', '50-150人']))]
    df_res = df.groupby('industry')['mean'].describe()
    df_j5_industry_salary = df_res[df_res['count'] > 10].sort_values('mean', ascending=False).apply(
        lambda x: round(x, 2))
    return pd.DataFrame(df_j5_industry_salary, columns=['mean', 'std']).to_json(orient='split', force_ascii=False)

# 智联 具体职位薪资排行
# @param type 1 只分析职位 2 加入工作年限和地区
# @param sort_type 1, 高到低 2， 低到高
def getZLSalaryByPosition(type = 1, sort_type = 1):
    sql = database.getZLSalaryByPositionSql()
    conn = database.getDatabaseConn()
    df = pd.read_sql(sql, conn)
    if type == 1:
        condition = ['position_type']
    elif type == 2:
        condition = ['position_type', 'work_year', 'city']
    sort_status = True if sort_type == 1 else False
    df_res = df.groupby(condition).describe().salary_high.sort_values('mean', ascending=sort_status)[:100]
    res = pd.concat([df_res['std'].apply(lambda x: int(x)), df_res['mean'].apply(lambda x: int(x)), df_res['50%'].apply(lambda x: int(x))], axis=1).rename(columns={'std':'标准差','mean':'平均值','50%':'中位数'})
    res.to_excel('output/PositionSalaryByWE.xlsx')
    return res.to_json(orient='index', force_ascii=False)

# 城市薪资排行
# @param type 1、全部 2、工作年限1-3的
def getCitySalary(type = 1):
    df_51 = job51SalaryPosition()
    df_lagou = lagouSalaryDetail()
    city_mix_df = pd.concat([pd.DataFrame(df_51, columns=['city', 'salary_mean', 'work_year']),
                             pd.DataFrame(df_lagou, columns=['city', 'salary_mean', 'work_year'])])
    if type == 1:
        g_df = city_mix_df.groupby('city')
        g_df_res = g_df.describe().apply(lambda x: round(x, 2))
        g_df_res[('salary_mean', 'mean')] = g_df_res[('salary_mean', 'mean')].apply(lambda x: x * 1000)
        g_df_res[('salary_mean', '50%')] = g_df_res[('salary_mean', '50%')].apply(lambda x: x * 1000)
        g_df_res = g_df_res[
            (g_df_res[('salary_mean', 'std')] < 20) & (g_df_res[('salary_mean', 'count')] > 18)].sort_values(
            ('salary_mean', 'mean'), ascending=False)

    else:
        g_df = city_mix_df[city_mix_df['work_year'] == '1-3年'].groupby('city')
        g_df_res = g_df.describe().apply(lambda x: round(x, 2))
        g_df_res[('salary_mean', 'mean')] = g_df_res[('salary_mean', 'mean')].apply(lambda x: x * 1000)
        g_df_res[('salary_mean', '50%')] = g_df_res[('salary_mean', '50%')].apply(lambda x: x * 1000)
        g_df_res = g_df_res[
            (g_df_res[('salary_mean', 'std')] < 20) & (g_df_res[('salary_mean', 'count')] > 5)].sort_values(
            ('salary_mean', 'mean'), ascending=False)


    res_df = pd.DataFrame(g_df_res, columns=[('salary_mean', 'std'), ('salary_mean', 'mean'),
                                             ('salary_mean', '50%')]).rename(
        columns={'salary_mean': '薪资/k', 'mean': '平均数', 'std': '标准差', '50%': '中位数', })

    return res_df

# 城市薪资排行转excel
def citySalaryToExcel(type = 1, path = "output/citySalary.xlsx"):
    df = getCitySalary(type)
    df.to_excel(path)

# echarts地图之城市薪资展示数据处理 TODO df格式不对
def citySalaryToEcharts(type = 1):
    df = getCitySalary(type)
    df_copy = pd.concat([df.index, df[('salary_mean', '50%')]], axis=1)
    import json
    res = str(json.loads(
        pd.DataFrame(df_copy, columns=['city', '中位数']).rename(columns={'city': 'name', '中位数': 'value'}).to_json(
            orient='index', force_ascii=False)).values()).replace("\'name\'", "name").replace("\'value\'", "value")
    return res