import pandas as pd
import datetime
from collections import Counter

# 实现功能：获取工作日全天未打卡日期、获取漏打卡日期、获取迟到日期
class dataAnalyze():
    date_list = []
    day_list = []
    workday_list = []

    def __init__(self,name):
        data = pd.read_excel('/Users/monstar/Desktop/2017.xlsx')
        data = data[(data['姓名'] == name)]
        name_list = set(list(data['姓名']))
        num = data.index[0]
        self.department = data['部门'][num]
        self.name = data['姓名'][num]
        self.marknum = data['考勤号码'][num]

        # 转换为日期
        for i in data.index:
            self.date_list.append(datetime.datetime.strptime(data['日期时间'][i], '%Y/%m/%d %H:%M:%S'))

        # 获取所有打卡天数
        for j in self.date_list:
            self.day_list.append(int(j.strftime('%d')))

        # 获取当月工作日日期
        self.current_year = self.date_list[0].year
        self.current_month = self.date_list[0].month
        first_date = str(self.current_year) + str(self.current_month)
        current_date = datetime.datetime.strptime(first_date, '%Y%m')
        for i in range(31):
            delta = datetime.timedelta(days=i)
            incr_date = current_date + delta
            if incr_date.month == self.date_list[0].month and int(incr_date.strftime('%w')) not in (0, 6):
                self.workday_list.append(incr_date.day)

    # 日期格式化：将天数转为xxxx-xx-xx格式的日期
    def dateFormat(self, deal_list):
        date_list = []
        for i in deal_list:
            date_format = datetime.datetime.strptime(str(self.current_year) + str(self.current_month) + str(i),
                                                     '%Y%m%d')
            date_list.append(date_format.strftime('%Y-%m-%d'))
        return date_list

    # 获取工作日全天未打卡日期
    def getHoleDay(self):
        res = set(self.workday_list) - set(self.day_list)
        return self.dateFormat(res)

    # 获取漏打卡日期
    def getMissingDate(self):
        day_count_dict = Counter(self.day_list)
        only_one = []
        res = {}
        day_mark = []

        # 获取只打卡一次的天数
        for key, item in day_count_dict.items():
            if item == 1:
                day_mark.append(key)

        # 获取当天早退日期
        mark = 0
        for key, item in enumerate(self.date_list):
            duration = int(item.strftime('%H')) - int(self.date_list[key - 1].strftime('%H'))
            day = item.strftime('%d')
            if mark == day and duration < 8:
                day_mark.append(int(day))
            mark = item.strftime('%d')

        mark_1 = 0
        # 获取异常日期的打卡记录
        for j in self.date_list:
            if int(j.strftime('%d')) in day_mark:
                # date日期
                if mark_1 != j.strftime('%d'):
                    res[j.strftime('%Y-%m-%d')] = []
                res[j.strftime('%Y-%m-%d')].append(j.strftime('%H:%M:%S'))
                mark_1 = j.strftime('%d')

        return res

    # 获取迟到日期
    def getLateDate(self):
        late_list = []
        for item in self.date_list:
            hour = int(item.strftime('%H'))
            minute = int(item.strftime('%M'))
            if  hour> 8 and hour < 11 and minute > 30:
                late_list.append(item.strftime("%Y-%m-%d %H:%M:%S"))
        return late_list



if __name__ == '__main__':
    name = input('请输入姓名：')
    dateres = dataAnalyze(name)
    title = '部门：{}  姓名：{}  员工号：{}'.format(dateres.department, dateres.name, dateres.marknum)
    print(title)
    print('*' * 50 + '缺勤日期' + '*' * 50)
    print()
    print(dateres.getHoleDay())
    print()
    print('*' * 50 + '打卡异常' + '*' * 50)
    print()
    for key,item in dateres.getMissingDate().items():
        print('日期：{} ，打卡记录：{}'.format(key, ','.join(item)))
    print()
    print('*' * 50 + '迟到日期' + '*' * 50)
    print()
    if len(dateres.getLateDate()) > 0:
        for item in dateres.getLateDate():
            print('日期：{}'.format(item))
    else:
        print('本月无迟到记录，继续保持哦！')