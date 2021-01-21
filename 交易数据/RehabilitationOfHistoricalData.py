import tushare as ts

#import 股票清单处理.StockDict as sd
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录 import profile as pf, date, function


class RehabilitationOfHistoricalData:
    # 初始化
    def __init__(self,StockNumber = "",QFQ = True ,YEAR =""):
        # 股票代码
        self.StockNumber = StockNumber
        # 前复权
        self.QFQ = QFQ
        #获取年份
        self.YEAR = YEAR
        # 文件存放的目录(老版本)
        self.RehabilitationOfHistoricalData = pf.GLOBAL_PATH + pf.SEPARATOR + pf.TransactionData + pf.SEPARATOR + pf.RehabilitationOfHistoricalData + pf.SEPARATOR
        # 文件存放的目录(新版本)
        self.HistoricalData = pf.GLOBAL_PATH + pf.SEPARATOR + pf.TransactionData + pf.SEPARATOR + pf.HistoryData + pf.SEPARATOR

    #################################################
    # 获取股票复权数据（一年的数据）
    #################################################
    def getRehabilitationOfHistoricalDataYear(self):
        try:
            startDay = self.YEAR + "-01-01"
            endDay = self.YEAR + "-12-31"
            if self.QFQ :
                print("%s%s %s" % ("\n获取前复权数据：",self.YEAR ,self.StockNumber))
                dir = '%s%s%s%s%s' % (self.RehabilitationOfHistoricalData, pf.Qfq, pf.SEPARATOR, self.YEAR, pf.SEPARATOR)
                filename = '%s%s%s' % (dir , self.StockNumber, pf.Execl)
                data = ts.get_h_data(self.StockNumber, autype='qfq', start=startDay, end=endDay)
                print("获取当年股票前复权数据   成功！")
            else:
                print("%s%s %s" % ("\n获取后复权数据：", self.YEAR, self.StockNumber))
                dir = '%s%s%s%s%s' % (self.RehabilitationOfHistoricalData, pf.Hfq, pf.SEPARATOR, self.YEAR, pf.SEPARATOR)
                filename = '%s%s%s' % (dir, self.StockNumber, pf.Execl)
                data = ts.get_h_data(self.StockNumber, autype='hfq',start=startDay, end=endDay)
                print("获取当年股票后复权数据   成功！")
            function.checkAndCreateDir(dir)
            data.to_excel(filename)
        except:
            print("获取当年股票复权数据失败！")

    #################################################
    # 获取股票历史复权数据（一年的数据）
    #################################################
    def getHistoricalDataYear(self):
        try:
            startDay = self.YEAR + "-01-01"
            endDay = self.YEAR + "-12-31"
            if self.QFQ:
                print("%s%s %s" % ("\n获取历史前复权数据：", self.YEAR, self.StockNumber))
                dir = '%s%s%s%s%s' % (self.HistoricalData, pf.Qfq, pf.SEPARATOR, self.YEAR, pf.SEPARATOR)
                filename = '%s%s%s' % (dir, self.StockNumber, pf.Execl)
                data = ts.get_k_data(self.StockNumber, autype='qfq', start=startDay, end=endDay)
                print("获取当年股票历史前复权数据   成功！")
            else:
                print("%s%s %s" % ("\n获取历史后复权数据：", self.YEAR, self.StockNumber))
                dir = '%s%s%s%s%s' % (self.HistoricalData, pf.Hfq, pf.SEPARATOR, self.YEAR, pf.SEPARATOR)
                filename = '%s%s%s' % (dir, self.StockNumber, pf.Execl)
                data = ts.get_k_data(self.StockNumber, autype='hfq', start=startDay, end=endDay)
                print("获取当年股票历史后复权数据   成功！")
            function.checkAndCreateDir(dir)
            data.to_excel(filename)
        except:
            print("获取当年股票历史复权数据失败！")

    #################################################
    # 获取股票复权数据（一年的数据）（包括前复权和后复权）
    #################################################
    def getRehabilitationOfHistoricalDataYearAll(self):
        try:
            instanceStock = RehabilitationOfHistoricalData(StockNumber=self.StockNumber, QFQ=True, YEAR=self.YEAR)
            #instanceStock.getRehabilitationOfHistoricalDataYear()
            instanceStock.getHistoricalDataYear()
            instanceStock.QFQ = False
            #instanceStock.getRehabilitationOfHistoricalDataYear()
            instanceStock.getHistoricalDataYear()
        except:
            print("获取当年股票复权数据失败！")

    #################################################
    # 获取股票复权数据（从起始年到终止年的数据）（包括前复权和后复权）
    # 入参1，起始年份 如：2015
    # 入参2，步长 如：2
    #################################################
    def getRehabilitationOfHistoricalDataFromBeginToEndYear(self,startYear,length):
        for year in range( int(startYear), int(startYear) + length ):
            self.YEAR = str(year)
            self.getRehabilitationOfHistoricalDataYearAll()

#################################################
# 获取所有股票所有复权数据和历史数据
#################################################
def getStockAllData():
    instanceStockDict = StockDict()
    for stockId in sorted(instanceStockDict.stockDict["timeToMarket"].keys()):#对股票代码进行排序，下面那句不排序
    #for stockId in instanceStockDict.stockDict["timeToMarket"]:
        yearAndLength = date.getYearLength(str(instanceStockDict.stockDict["timeToMarket"][stockId]))
        if yearAndLength[0]:
            aa = RehabilitationOfHistoricalData(StockNumber = stockId)
            aa.getRehabilitationOfHistoricalDataFromBeginToEndYear(yearAndLength[1],yearAndLength[2])


#################################################
# 获取所有股票，某一年份的后复权数据
# 入参：年：2016
#################################################
def getStockYearData(year,qfq=False):
    instanceStockDict = StockDict()

    aa = RehabilitationOfHistoricalData(StockNumber="", QFQ=qfq,YEAR=str(year) )
    for stockId in sorted(instanceStockDict.stockDict[pf.股票清单表头[1]].keys()):  # 对股票代码进行排序，下面那句不排序
    #for stockId in instanceStockDict.stockDict["timeToMarket"]:
        aa.StockNumber = stockId
        aa.getHistoricalDataYear()

if __name__ == '__main__':

    #获取所有数据，第一次使用
    #getStockAllData()
    pass
