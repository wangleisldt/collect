import datetime
import math

#################################################
# 根据当前时间的年份
#################################################
def getCurrentYear():
    year = int(datetime.datetime.now().strftime('%Y'))
    return year

#################################################
# 根据当前时间的月份
#################################################
def getCurrentMonth():
    month = int(datetime.datetime.now().strftime('%m'))
    return month

#################################################
# 根据当前时间获取当前的季度
#################################################
def getCurrentQuarter():
    quarter = math.ceil(getCurrentMonth()/3)
    return quarter

#################################################
# 根据当前时间获取当年的季度（如果是三季度，则返回1,2）
#################################################
def getCurrentQuarterList():
    quarter = int(getCurrentMonth()/3)
    quarterList = []
    for i in range(1,quarter+1):
        quarterList = quarterList + [i]
    return quarterList

#################################################
# 获取当前日期 2017-08-31
#################################################
def getCurrentDate():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return date

#################################################
# 根据日期返回到当年有几年
# 入参 日期  20150831
# 返回 如当年是2017年 则 返回 True 2015 3
#################################################
def getYearLength(date):
    year = datetime.datetime.now().strftime('%Y')
    if len(date) != 1:
        yearDate =  date[0:4]
        return True,yearDate,int(year) - int(yearDate) + 1
    else:
        return False,"0000",1

#################################################
# 计算给定年月之前几个季度的年月
# 入参 日期  2015
# 入参 季度 3
# 入参 前面几个季度
# 返回 如当年是2017，3 ，6 则 返回 20161
#################################################
def getYearQuarterMinusQuarter(date,quaterIn,length):
    year = int(date)
    quater = int(quaterIn)
    year = year - length // 4
    if quater - (length % 4) <= 0 :
        year = year -1
        quater = quater - (length % 4) +4
    else:
        quater = quater - (length % 4)
    return(str(year)+str(quater))

#################################################
# 计算给定年月之后的年月
# 入参 日期  201508
# 入参 月份数量  3
# 返回 如当年是201703，3 则 返回 201706
#################################################
def getYearMonthFromMonthLength(date,length):
    year = int(date[0:4])
    month = int(date[4:6])
    year = year + length // 12
    if month + (length % 12) > 12:
        year = year +1
        month = month + (length % 12) - 12
    else:
        month = month + (length % 12)

    if month<10:
        return str(year)+"0"+str(month)
    else:
        return str(year) +str(month)

#################################################
# 计算当前日期前2个季度
# 返回 如果当前是  20150803 则 返回 2015,1
#################################################
def get_current_2_quarter_before():
    year = getCurrentYear()
    quarter = getCurrentQuarter()
    if  quarter == 1:
        year = year - 1
        quarter = 3
    elif quarter == 2:
        year = year - 1
        quarter = 4
    else:
        quarter = quarter - 2
    return year,quarter

#################################################
# 计算给定日期的前一个季度
# 入参 日期  2015
# 入参 月份数量  1
# 返回 2014,4
#################################################
def get_1_quarter_before(year,quarter):
    if  quarter == 1:
        year = year - 1
        quarter = 4
    else:
        quarter = quarter - 1
    return year,quarter

#################################################
# 计算给定日期的前一个季度
# 入参 日期  2015
# 入参 月份数量  1
# 返回 2015,2
#################################################
def get_1_quarter_after(year,quarter):
    if  quarter == 4:
        year = year + 1
        quarter = 1
    else:
        quarter = quarter + 1
    return year,quarter

#################################################
# 给定一天，计算后几天
# 入参 日期  20151231
# 入参 增加几天  1
# 返回 20160101
#################################################
def 后几天(date,add_day):
    date_time = "%s %s" % (date,"00:00:00")
    d1 = datetime.datetime.strptime(date_time, '%Y%m%d %H:%M:%S')
    delta = datetime.timedelta(days=add_day)
    n_days = d1 + delta
    return str(n_days.strftime('%Y%m%d'))

if __name__ == '__main__':
    print(getCurrentYear(),getCurrentMonth(),getCurrentQuarter())
    print(getCurrentQuarterList())
    print(getCurrentDate())
    print(getYearLength("20160831"))
    print(getYearQuarterMinusQuarter("2017","3",6))
    print(getYearMonthFromMonthLength("201503",34))
    print(后几天("20181231",2))
    print(get_1_quarter_after(2020,4))




