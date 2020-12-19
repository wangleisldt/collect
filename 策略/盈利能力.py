import pandas as pd

import 交易数据.实时交易数据 as sp
import 函数目录.CalculateFuncation as cal
import 基本面数据.FundamentalExeclToDict as fetd
import 策略.获取文件数据到字典 as ftd
import 股票清单处理.StockDict as sd
from 函数目录 import profile as pf


class GrowthPolicy():
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
        self.stockGrowthList = []

        #遍历股票清单与Growth文件，将数据存放到stockGrowthList
        self.GrowthAbilityImport()

    ################################################
    #
    ################################################
    def GrowthAbilityImport(self):
        if self.Type == "Year":
            output = ftd.getFundamentalDataToDictYear(Type=pf.GrowthAbility, Year=self.Year, Length=self.Length,Quarter=self.Quarter)  # 先获取要处理的数据
        else:
            output = ftd.getFundamentalDataToDictYearQuarter(Type=pf.GrowthAbility, Year=self.Year, Length=self.Length,Quarter=self.Quarter)  # 先获取要处理的数据

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

                # 进一步获取净利润增长和主营增长-净利润增长两组数据
                for element in list1:
                    nprg = element[1][3].strip()
                    if nprg != "":
                        contentList.append(round(float(nprg), 4))
                        mbrg = element[1][2].strip()
                        if mbrg != "":
                            mbrg = float(mbrg)
                            nprg = float(nprg)
                            contentList.append(round(mbrg - nprg, 4))
                            # else:
                            # mbrg = 0
                            # nprg = float(nprg)
                            # contentList.append(round(mbrg - nprg, 4))
                            # 到此步，获得类似这样的数据，其中第一个为第一年的净利润增长，第二为主营增长-净利润增长 ，两两一组 ['002630', '华西能源', 13.469, -9.2735, 36.8691, -23.6783, 0.1956, -8.2833]

            # 如果数据有缺失则不加入最终的List
            if len(contentList) == 2 + 2 * self.Length:
                self.stockGrowthList.append(contentList)

    ################################################
    #
    ################################################
    def GrowthAbilityCalculate(self):
        # 对增长数据list进行处理
        self.processGrowthList()
        #for element in self.stockGrowthList:
            #print(element)

        return self.createDataFrame()

    ################################################
    #
    ################################################
    def processGrowthList(self):

        instanceStockPrice = sp.realtimeStockPrice() #初始化股票实时价格查询类，方便后续查询
        earningsDict = self.getAllEarningsToDict() #将每股收益放入字典供后续查询

        for element in self.stockGrowthList:
            stockId = element[0]
            try:
                earnings = float(earningsDict[0][stockId][earningsDict[1]][6])
            except:
                earnings = 0

            # print(element)
            growthList = self.getCalList(element, self.Length, 0)
            # for element1 in growthList:
            # print(element1)

            avg = round(cal.calListAvg(growthList), 6)
            stdev = round(cal.calListStdev(growthList), 6)
            mbrgMinusNprgList = self.getCalList(element, self.Length, 1)
            stdevMbrgMinusNprg = round(cal.calListStdev(mbrgMinusNprgList), 6)
            # 计算预测增长率（最近2个数据平均占70%，剩余平均占30%）
            forecastGrowth = self.calForecastGrowth(growthList)

            # 将结果加入到队尾
            # 平均增长
            element.append(avg)
            # 利润增长偏离
            element.append(stdev)
            # 销售收入与利润差的偏离
            element.append(stdevMbrgMinusNprg)
            # 利润增长偏离与销售收入与利润差的偏离的平均
            element.append(round(cal.calListAvg([stdev, stdevMbrgMinusNprg]), 6))
            # 计算预测增长率（最近2个数据平均占70%，剩余平均占30%）
            element.append(forecastGrowth)
            # 计算预测增长率与平均盈利增长的偏离
            element.append(round(cal.calListStdev([forecastGrowth, avg]), 6))

            #股票当前收盘价
            closingPrice = instanceStockPrice.getRealtimeStockPrice(stockId)
            element.append(closingPrice)
            # 股票的每股收益（根据去年）
            element.append(earnings)
            #股票的市盈率（根据当前价计算）
            if earnings != 0:
                eps = round(closingPrice/earnings,6)
            else:
                eps = 0
            element.append(eps)
            #股票的PEG
            peg = round(eps/forecastGrowth,6)
            element.append(peg)




    ################################################
    #
    ################################################
    def createDataFrame(self):
        length = self.Length
        index = []
        for element in self.stockGrowthList:
            index.append(element)

        dict = {}
        for element in self.stockGrowthList:
            dict[element[0]]=pd.Series(element)

        returnDataframe = pd.DataFrame(dict).T

        #修改列名
        returnDataframe.rename(columns={0: '股票代码', 1: '股票名称',2+length*2:'利润平均增长',2+length*2+1:'利润增长偏离' , 2 + length * 2 + 2: '销售收入与利润差的偏离', 2 + length * 2 + 3: '利润增长偏离与销售收入与利润差的偏离的平均', 2 + length * 2 + 4: '预测增长率', 2 + length * 2 + 5: '预测增长与前面平均增长偏离'}, inplace=True)
        # 修改列名
        returnDataframe.rename(columns={2 + length * 2 + 6:'当前收盘价'}, inplace=True)
        returnDataframe.rename(columns={2 + length * 2 + 7: '每股收益（根据去年）'}, inplace=True)
        returnDataframe.rename(columns={2 + length * 2 + 8: '股票的市盈率（根据当前价计算）'}, inplace=True)
        returnDataframe.rename(columns={2 + length * 2 + 9: '股票的PEG'}, inplace=True)

        return returnDataframe

    ################################################
    # 从返回的list获取增长数据，保存到list
    ################################################
    def getCalList(self,list,length,start):
        returnList = []
        for i in range(0,length):
            returnList.append(list[2+2*i+start])
        return  returnList

    ################################################
    #
    ################################################
    def calForecastGrowth(self,growthList):

        #根据增长率list，模拟计算增长率
        #计算方法，将增长率两两求和平均，然后根据最近的增长率*70%+之前的增长率平均*30%来模拟推断增长率
        outputList = []
        length = len(growthList)
        for i in range( 0 ,length-1):
            outputList.append(round(cal.calListAvg([growthList[i],growthList[i+1]]),6))
        #print(outputList)
        length = len(outputList)
        headList = cal.calListAvg(outputList[:length-1])
        last = outputList[length-1]

        #print(headList)
        return round((headList*0.3 + last*0.7),6)

    ################################################
    # 将根据当前年份，获取上年的盈利数据字典，方便后续查询
    ################################################
    def getAllEarningsToDict(self):
        if self.Quarter == "4":
            year = self.Year
        else:
            year = str( int(self.Year) - 1 )

        dir = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.ProfitAbility + pf.SEPARATOR
        #filename = dir + year +self.Quarter+pf.Execl
        instance = fetd.FundamentalExeclToDict(DirName=dir, Year=year, Length=1, Quarter="4")
        instance.getRangeDataYearToDict()
        return instance.OutputDict,year+"4"



if __name__ == '__main__':
    #获取股票清单列表
    stockIdListInstance = sd.StockDict()
    # 对这批股票清单进行处理，季度
    #growthAbilityListInstance = GrowthPolicy( StockIdList=stockIdListInstance.stockIdList , Year="2017", Length=8, Quarter="4" ,Type = "Quator")
    growthAbilityListInstance = GrowthPolicy(StockIdList=stockIdListInstance.stockIdList, Year="2019", Length=8,
                                             Quarter="2", Type="Quator")

    # 对这批股票清单进行处理，年度
    #growthAbilityListInstance = GrowthPolicy(StockIdList=stockIdListInstance.stockIdList, Year="2017", Length=8,Quarter="2", Type="Year")

    aa = growthAbilityListInstance.GrowthAbilityCalculate()


    aa.to_excel("c:\\盈利能力结果2019-02.xlsx")

