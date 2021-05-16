# encoding:utf-8

import time
import pandas as pd
from 函数目录 import profile as ct
from 函数目录 import function as fn
from 数据采集.股票清单.股票清单获取 import StockDict
from 数据采集.财务分析.采集标准类 import 获取_财务分析表,获取某季度财务分析数据

URL = ct.财务指标_URL
TABLE_XPATH = "//table[@id='BalanceSheetNewTable0']/tbody/tr"

def 全量获取(year, quarter,dict_has_get_all):
    # 初始化全部股票代码
    stockListInstance = StockDict()
    return_dict = {}

    for element in stockListInstance.stockIdList:
        try:

            print("开始获取%s股票的%s年%s季度的--财务指标--数据。" % (element, year, quarter))
            #判断是否获取过
            if element in dict_has_get_all.keys():
                print("之前已获取过相关数据")
            else:
                df = 获取_财务指标(year, quarter, element)
                if df is not None:
                    return_dict[element]=df
                    # print(df)
                else:
                    print("%s无相关数据。" % element)
        except:
            print("获取%s失败################################################" % element)

    #将采集的数据与之前在文件中读取的数据进行合并
    return_dict.update(dict_has_get_all)
    return return_dict

def 保存数据(dict,year, quarter):
    print("开始保存数据")
    dirname = ct.GLOBAL_PATH + ct.SEPARATOR + ct.FUNDAMENTAL_DATA + ct.SEPARATOR + ct.FinancialIndex + ct.SEPARATOR
    fn.checkAndCreateDir(dirname)
    filename = "%s-%s.xlsx" % (year, quarter)
    fn.将字典保存成Execl文件(dict, dirname + filename)
    print("结束保存数据")



def 获取_财务指标(year, quarter ,stockId):

    def process_dataframe(df):
        for i in range(0, len(df.columns)):
            date = str(year) + ct.End_OF_SEASON_DAY[quarter]
            if date == df[i][0]:
                return df.loc[:, [0, i]]
        return None

    if ct._check_input(year, quarter ) is True:
        df = 获取_财务分析表(URL , year, quarter,stockId, 1, pd.DataFrame(),TABLE_XPATH)
        if df is not None:
            return process_dataframe(df)
        else:
            return None

def 全流程(year, quarter):
    dict_has_get_all = 获取某季度财务分析数据(ct.FinancialIndex,year, quarter)
    dict = 全量获取(year, quarter,dict_has_get_all)
    保存数据(dict, year, quarter)

def 获取_全量股票_财务指标_某个季度(year,quarter):
    全流程(year, quarter)



if __name__ == '__main__':
    #df = 获取_财务指标(2016,2 , 601006)

    #dirname = ct.GLOBAL_PATH + ct.SEPARATOR + ct.FUNDAMENTAL_DATA + ct.SEPARATOR + ct.FinancialIndex + ct.SEPARATOR + "temp"
    #filename = "601006-2016-2.xlsx"
    #save_file_dataframe_to_execl(dirname,filename,df)

    #stockId, success_year, success_quarter = 获取_全量_财务指标(601006)
    #print("%s最后一次正确获得财务数据是：%s年%s季度。" % (stockId, success_year, success_quarter))


    ##################################
    #  一般使用下面的函数
    ##################################
    #获取_全量股票_财务指标()

    获取_全量股票_财务指标_某个季度(2020,4)

