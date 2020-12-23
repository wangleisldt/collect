from 函数目录 import profile as pf
from 数据采集.股票清单.股票清单获取 import StockDict
import pickle
import pandas as pd
from 函数目录.date import getYearMonthFromMonthLength


class 上市公司调研情况月度数据处理:
    # 初始化
    def __init__(self, yearMonth):
        self.yearMonth = yearMonth  #要整理的月度201805
        self.dict = {}
        self.returnDict = {}

        # 产生需要打开的目录
        self.base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        self.dirname = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.汇总数据, pf.SEPARATOR)

        self.从文件中读取字典()
        self.通过字典进行汇总返回汇总字典()
        #self.将字典生成EXECL()

    #从之前的原始数据（pkl）文件读取数据到dict中
    def 从文件中读取字典(self):


        fullfilename = '%s%s%s' % (self.dirname,self.yearMonth,pf.PklFile)

        pklFile = open(fullfilename, 'rb')
        self.dict = pickle.load(pklFile)
        pklFile.close()

    def 通过字典进行汇总返回汇总字典(self):
        def 根据key获取股票代码(filename):
            stockid = key.split('_')[0]
            return stockid

        for key in self.dict:
            stockid = 根据key获取股票代码(key)
            if self.returnDict.get(stockid) is None:
                self.returnDict[stockid] = self.dict[key]
            else:
                self.returnDict[stockid] = self.returnDict[stockid] + self.dict[key]

    def 将字典生成EXECL(self):
        stockdict = StockDict()
        接收list = []
        for key in self.returnDict:
            接收list.append([key, stockdict.stockDict['name'][key],self.returnDict[key]])

            接收list = sorted(接收list, key=lambda stock: stock[0])

        # 根据list产生dataframe
        filename = self.dirname + self.yearMonth + pf.Execl
        df = pd.DataFrame(接收list, columns=['股票代码', '股票名称', '调研次数'])
        df.to_excel(filename)

        #print(df)

        #for element in 接收list:
            #print(element)

    def 字典打印输出(self):
        for key in self.returnDict:
            print(key, self.returnDict[key])

def 上市公司调研情况月度数据合并处理接口(startDate,monthLength):
    for i in range(0, int(monthLength)):
        yearMonth = getYearMonthFromMonthLength(startDate, i)
        上市公司调研情况月度数据处理instance = 上市公司调研情况月度数据处理(yearMonth)
        上市公司调研情况月度数据处理instance.将字典生成EXECL()


if __name__ == '__main__':
    上市公司调研情况月度数据合并处理接口('201807', 1)

