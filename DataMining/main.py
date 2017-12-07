from dataMiningFunc import *

if __name__ == '__main__':
    lg_df_programing_rank = lagouRecruitCodeRank()
    lg_df_programing_rank.to_csv('/Users/monstar/Desktop/a.csv', encoding='gbk')