from 函数目录 import profile as pf
from 函数目录.function import checkAndCreateDir
from 函数目录.date import getYearMonthFromMonthLength

from 股票清单处理.StockDict import StockDict
import pandas as pd

from 数据采集.上市公司调研情况.数据汇总 import 上市公司调研情况月度数据处理

class 数据展现():
    # 初始化
    def __init__(self, startDate,monthLength):
        self.startDate = startDate  #201808
        self.monthLength = monthLength #几个月（步长）

        self.dict = {}  #存放月度数据，每个月的所有股票数据作为一条记录，然后这个数据里面再是具体的数据
        self.yearMonthList = []
        self.list = []#存放需要输出的list

        # 产生需要打开的目录
        self.base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        self.dirname_展现 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.展现数据, pf.SEPARATOR)
        self.dirname_汇总 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.汇总数据, pf.SEPARATOR)
        checkAndCreateDir(self.dirname_展现)
        self.产生需要处理的yearMonthList()


    def 产生需要处理的yearMonthList(self):
        for i in range( 0 ,int(self.monthLength)):
            yearMonth = getYearMonthFromMonthLength(self.startDate, i)
            self.yearMonthList.append(yearMonth)
        self.yearMonthList.sort()

    def 读取月度数据到字典(self):
        for element in self.yearMonthList:
            instance = 上市公司调研情况月度数据处理(element)
            self.dict[element] = instance.returnDict

        #print(self.dict)

    def 生成要展现的list(self):
        #获取股票清单
        stockdict = StockDict()

        #print(self.dict['201802']['002831'])

        #print(stockdict.stockDict)

        for stockId in stockdict.stockDict["timeToMarket"]:
            countList = []
            #sum = 0
            for yearMonth in self.yearMonthList:
                count = self.dict[yearMonth].get(stockId,0)
                countList.append(count)

            if sum(countList) != 0:
                list = []
                list.append(stockId)
                list.append(stockdict.stockDict['name'][stockId])
                list = list + countList
                list.append(sum(countList))
                self.list.append(list)


    def 将list生成文件(self):
        filename = '%s-%s%s' % (self.startDate,self.monthLength,pf.Execl)

        column_name = ['股票代码', '股票名称'] + self.yearMonthList + ['汇总数据']

        fullfilename = self.dirname_展现+filename
        df =pd.DataFrame(self.list, columns=column_name)
        df = df.sort_values(axis=0, ascending=False, by='汇总数据')
        df.to_excel(fullfilename)

        print('整理后的数据文件为：\n%s\n' % (fullfilename))


    def 数据展现(self):
        pass

def  数据展现接口(startDate,monthLength):
    instance = 数据展现(startDate,monthLength)
    instance.读取月度数据到字典()
    instance.生成要展现的list()
    instance.将list生成文件()


if __name__ == '__main__':
    数据展现接口('201807',1)
