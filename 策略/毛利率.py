import pandas as pd

import 交易数据.实时交易数据 as sp
import 函数目录.CalculateFuncation as cal
import 基本面数据.FundamentalExeclToDict as fetd
import 策略.获取文件数据到字典 as ftd
#import 股票清单处理.StockDict as sd
from 函数目录 import profile as pf
from 数据采集.股票清单.股票清单获取 import StockDict as sd

class  GrossProfitRatePolicy():
    # 初始化
    def __init__(self,StockIdList,Year, Length, Quarter,Type = "Year"):
        #要处理的股票清单
        self.StockIdList = StockIdList
        # 年
        self.Year = Year
        # 几年或者几个季度
        self.Length = Length
        # 季度
        self.Quarter = Quarter
        # 类型
        self.Type = Type
        # 存放结果
        self.stockGrossProfitRateList = []

        #遍历股票清单与Growth文件，将数据存放到stockGrowthList
        self.GrossProfitRateImport()

    ################################################
    #
    ################################################
    def GrossProfitRateImport(self):
        if self.Type == "Year":
            output = ftd.getFundamentalDataToDictYear(Type=pf.ProfitAbility, Year=self.Year, Length=self.Length,Quarter=self.Quarter)  # 先获取要处理的数据
        else:
            output = ftd.getFundamentalDataToDictYearQuarter(Type=pf.ProfitAbility, Year=self.Year, Length=self.Length,Quarter=self.Quarter)  # 先获取要处理的数据

        # 遍历股票代码list，取出一个股票代码，去output查询相关数据，存放到stockGrowthList
        for element in self.StockIdList:
            contentList = []
            if output.get(element, None) != None and len(output[element]) == self.Length:
                # print(element, '-----', output[element])
                dic = output[element]  # 从字典里面获取值
                list1 = sorted(dic.items(), key=lambda asd: asd[0], reverse=False)  # 对字典进行排序

                # 将股票代码和股票名称放入contenList
                contentList.append(element)  # 添加股票代码
                contentList.append(list1[1][1][1])  # 添加股票名称

                # 进一步获取毛利率数据
                for element in list1:
                    gross_profit_rate = element[1][4].strip()
                    if gross_profit_rate != "":
                        contentList.append(round(float(gross_profit_rate), 4))

            # 如果数据有缺失则不加入最终的List
            if len(contentList) == 2 + 1 * self.Length:
                self.stockGrossProfitRateList.append(contentList)


    ################################################
    #
    ################################################
    def GrossProfitRateCalculate(self):
        # 对数据list进行处理
        self.processGrossProfitRate()
        #for element in self.stockGrowthList:
            #print(element)

        return self.createDataFrame()

    ################################################
    #
    ################################################
    def processGrossProfitRate(self):

        for element in self.stockGrossProfitRateList:

            growthList = self.getCalList(element, self.Length, 0)

            avg = round(cal.calListAvg(growthList), 6)
            stdev = round(cal.calListStdev(growthList), 6)

            # 将结果加入到队尾
            # 平均增长
            element.append(avg)
            # 利润增长偏离
            element.append(stdev)



    ################################################
    #
    ################################################
    def createDataFrame(self):
        length = self.Length
        index = []
        for element in self.stockGrossProfitRateList:
            index.append(element)

        dict = {}
        for element in self.stockGrossProfitRateList:
            dict[element[0]]=pd.Series(element)

        returnDataframe = pd.DataFrame(dict).T

        # 修改列名
        returnDataframe.rename(columns={0: '股票代码'}, inplace=True)
        returnDataframe.rename(columns={1: '股票名称'}, inplace=True)

        returnDataframe.rename(columns={2 + length * 1 + 0:'平均'}, inplace=True)
        returnDataframe.rename(columns={2 + length * 1 + 1: '偏离'}, inplace=True)

        return returnDataframe

    ################################################
    # 从返回的list获取增长数据，保存到list
    ################################################
    def getCalList(self,list,length,start):
        returnList = []
        for i in range(0,length):
            returnList.append(list[2+1*i+start])
        return  returnList

if __name__ == '__main__':
    #获取股票清单列表
    stockIdListInstance = sd()

    # 对这批股票清单进行处理，季度
    GrossProfitRateListInstance = GrossProfitRatePolicy( StockIdList=stockIdListInstance.stockIdList , Year="2021", Length=18, Quarter="2" ,Type = "Quator")

    # 对这批股票清单进行处理，年度
    #growthAbilityListInstance = GrowthPolicy(StockIdList=stockIdListInstance.stockIdList, Year="2017", Length=8,Quarter="2", Type="Year")

    aa = GrossProfitRateListInstance.GrossProfitRateCalculate()
    print(aa)

    aa.to_excel("/home/wangleisldt/毛利率1.xlsx")
