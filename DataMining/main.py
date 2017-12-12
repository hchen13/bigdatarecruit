from dataMiningFunc import *

if __name__ == '__main__':
    ######################### 编程语言排行 #########################
    # # lagou
    # lagou_df_programing_rank_json = lagouRecruitCodeRank()
    # # zhilian
    # zhilian_df_programing_rank_json = zhilianPositionCodeRank()
    # # job51
    # job51_df_programing_rank_json = job51PositionRank()

    # 51排行前60的行业
    # Industry_num = get51IndustryNum()

    # 获取51职位排名
    # print(job51PositionRank())
    # 获取智联职位排名
    # print(zhilianPositionRank())
    #获取拉钩职位排行
    # print(lagouPositionRank())

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
    print(job51CompanyHighNumType(1))