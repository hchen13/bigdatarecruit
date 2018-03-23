from dataMiningFunc import *
from wordCloud import *

if __name__ == '__main__':
    # *********************************  编程语言排行  ********************************
    # # lagou
    # lagou_df_programing_rank_json = lagouRecruitCodeRank()

    # # zhilian
    # zhilian_df_programing_rank_json = zhilianPositionCodeRank()
    # print(zhilian_df_programing_rank_json)

    # # job51
    # job51_df_programing_rank_json = job51PositionRank()

    # 51排行前60的行业
    # Industry_num = get51IndustryNum()
    # print(Industry_num)

    # *********************************  行业招聘数分析  ********************************
    # 获取51职位排名
    # print(job51PositionRank())

    # 获取智联职位排名
    # print(zhilianPositionRank())

    #获取拉钩职位排行
    # print(lagouPositionRank())

    # *********************************  hr数据分析  ********************************
    # hr各时段处理简历的数量
    # hr_deal_time_json = hrRecruitTime()

    # 统计hr数量在前100的公司
    # print(lagouCompanyHrNum())

    # 统计hr数量在前100的公司规模占比
    # print(lagouCompanySizeByHrNum())

    # 统计hr数量在前100的公司类型占比
    # lagouCompanySizeByHrNum()

    # *********************************  公司招聘职位数排行  ********************************
    # 智联公司招聘职位数
    # print(zhilianCompanyPositionNum())

    # 智联公司招聘职位数
    # print(job51CompanyPositionNum())

    # 招聘职位前100里，公司规模占比
    # print(job51CompanyHighNumType(1))

    # *********************************  招聘工作年限职位数排行  ********************************
    # 智联
    # print(zhilianWorkYearNum())

    # 51job
    # print(j5WorkYearNum())

    # 获取51job教育程度招聘数情况
    # print(get51jobRecruitNumByEducation())

    # *********************************  拉钩薪资分布  ********************************

    # 拉钩
    # print(lagouWorkYearNum())

    # 拉钩整体薪资分布
    # print(lagouWholeSalaryDistribution())

    # 拉钩年限薪资分析
    # lagouWorkYearSalary()

    # 拉钩年限 标准差 分析
    # print(lagouWorkYearSalary(2))

    # *********************************  51job薪资情况（以下分析运行时间将近15分钟）  ********************************

    # 获取51job整体薪资中位数
    # print(get51jobSalaryMiddle(2))

    # 获取51job教育程度与薪资关系
    # print(get51jobSalaryByEducation())

    # 51job工作年限与薪资关系
    # print(get51jobSalaryByWorkYear())

    # 51job根据教育水平和工作年限分析薪资情况
    # print(get51jobSalaryByWE())

    # 51job行业薪资情况
    # list_key,list_mean, list_std = get51jobSalaryByIndustry()

    # 51job行业薪资标准差情况
    # get51jobSalaryStdByIndustry(2)

    # 智联 具体职位薪资排行前100
    # getZLSalaryByPosition(type = 2, sort_type=0)

    # 智联 具体职位薪资（年限，城市）排行前100
    # getZLSalaryByPosition(2)

    # 获取51job职位诱惑词云
    # getJ5PositionWordCloud()

    # 城市薪资排行
    # 1、全部 2、工作年限1-3的
    # print(citySalaryToExcel(type=2))

    # *********************************  词云  ********************************
    #获取拉钩职位词云
    getLagouPositionWordCloud('c++', type=1)
    # getWordCloud(content='/Users/monstar/Desktop/a.txt', type=2, status=1, temple_pic_path='/Users/monstar/Desktop/cube.jpg')