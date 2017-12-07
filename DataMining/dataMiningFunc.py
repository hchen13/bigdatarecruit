from tool import database, helper
import pandas as pd

# 统计hr各时段处理简历的数量
def hrRecruitTime():
    res = database.getLagouHrActiveTime()
    d = pd.DataFrame(res, columns = ['id', 'time'])
    data = d[d.time != '暂无']
    res = data.groupby('time').size().sort_values()
    return res.to_json(orient='index', force_ascii=False)

# 统计51job各行业职位数辆
def get51IndustryNum():
    res = database.get51IndustryNum()
    data = pd.DataFrame(res, columns=['industry', 'position_labels'])
    data = data[(True ^ data.industry.isin(['1000-5000人', '5000-10000人', '500-1000人', '少于50人', '150-500人', '50-150人']))]
    data_sort = data.groupby('industry').size().sort_values()
    res = data_sort[len(data_sort) - 50: len(data_sort)]
    return res.to_json(orient='index', force_ascii=False)

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

# 统计拉钩招聘职位中编程语言排行
def lagouRecruitCodeRank():
    # 获取拉钩的sql
    sql = database.getLagouPositionSql()
    # 获取数据库连接
    conn = database.getDatabaseConn()
    # 获取常用语言
    programing_language_list = helper.getProgramingLanguage()
    # 获取数据
    lg_rd_df = pd.read_sql(sql, conn)
    conn.close()
    query_key = ['position_name', 'position_labels']
    # 查询数据
    lg_df_programing_rank = getNumByKeyWords(lg_rd_df, query_key, programing_language_list)
    return lg_df_programing_rank

# 获取智联招聘编程语言排行