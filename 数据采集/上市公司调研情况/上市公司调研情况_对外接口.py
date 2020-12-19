from 数据采集.上市公司调研情况.获取上市公司调研情况 import 获取上市公司调研情况_根据股票代码一个一个获取
from 数据采集.上市公司调研情况.上市公司调研情况数据整理 import 上市公司调研情况月度数据处理
from 函数目录.date import getCurrentYear,getCurrentMonth

#def 上市公司调研情况全量获取(from_stockid = '000000'):
    #a = 获取上市公司调研情况_根据股票代码一个一个获取()#初始化类
    #a.根据全量股票进行获取(from_stockid = from_stockid)#这个是支持断点续取的

def 上市公司调研情况全量获取():
    a = 获取上市公司调研情况_根据股票代码一个一个获取()#初始化类
    a.根据全量股票进行获取()#这个是支持断点续取的

def 上市公司调研情况数据整理(yearmonth = 0):
    a = 上市公司调研情况月度数据处理()
    a.数据汇总_步骤一()
    if yearmonth != 0:#当入参指定的年月
        a.数据汇总_步骤二(yearmonth)
    else:
        #如果根据当前时间，分别整理汇总当月与上个月的数据
        year = getCurrentYear()
        month = getCurrentMonth()
        a.数据汇总_步骤二(year*100+month)
        month = month -1
        if month == 0:
            month = 12
            year = year -1
        a.数据汇总_步骤二(year * 100 + month)

def 数据展示(yearmonth,length):#入参如   （201801,6）代表从201801开始的6个月的数据展示
    a = 上市公司调研情况月度数据处理()
    a.数据展示(yearmonth,length)

def 上市公司调研情况全量获取加数据整理():
    上市公司调研情况全量获取()
    上市公司调研情况数据整理()

if __name__ == '__main__':
    #上市公司调研情况全量获取()
    上市公司调研情况数据整理()
    #数据展示(201801, 12)