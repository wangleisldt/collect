# encoding:utf-8

import time
import requests
# from urllib.request import urlopen, Request
# import lxml.html
from lxml import etree
# from pandas.compat import StringIO
import pandas as pd

from 函数目录 import profile as ct
from 函数目录 import function as fn
from 数据采集.股票清单.股票清单获取 import StockDict
from 数据采集.财务分析.采集标准类 import 获取_财务分析表,获取某季度财务分析数据

URL = ct.公司利润表_URL
TABLE_XPATH = "//table[@id='ProfitStatementNewTable0']/tbody/tr"

def 全量获取(year, quarter,dict_has_get_all):
    # 初始化全部股票代码
    stockListInstance = StockDict()
    # 对每个股票代码进行处理
    count = 0
    sleep_stock_num = 500
    sleep_sec = 5
    return_dict = {}

    for element in stockListInstance.stockIdList:
        # if count == sleep_stock_num:
        #     print('网页查询了%s个股票等待%s秒！' % (sleep_stock_num, sleep_sec))
        #     time.sleep(sleep_sec)
        #     count = 0
        # else:
        #     count = count + 1
            # time.sleep(1)

        try:

            print("开始获取%s股票的%s年%s季度的--公司利润表--数据。" % (element, year, quarter))
            #判断是否获取过
            if element in dict_has_get_all.keys():
                print("之前已获取过相关数据")
            else:
                df = 获取_公司利润表(year, quarter, element)
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
    dirname = ct.GLOBAL_PATH + ct.SEPARATOR + ct.FUNDAMENTAL_DATA + ct.SEPARATOR + ct.CompanyProfitStatement + ct.SEPARATOR
    filename = "%s-%s.xlsx" % (year, quarter)
    fn.将字典保存成Execl文件(dict, dirname + filename)
    print("结束保存数据")



def 获取_公司利润表(year, quarter ,stockId):

    def process_dataframe(df):
        for i in range(0, len(df.columns)):
            date = str(year) + ct.End_OF_SEASON_DAY[quarter]
            if date == df[i][0]:
                #print(df[i][0])
                #print(i)
                #return df[0]
                return df.loc[:, [0, i]]
        return None

    if ct._check_input(year, quarter ) is True:
        # ct._write_head()
        df = 获取_财务分析表(URL , year, quarter,stockId, 1, pd.DataFrame(),TABLE_XPATH)
        # df = _获取_公司利润表(year, quarter,stockId, 1, pd.DataFrame())
        if df is not None:
            return process_dataframe(df)
        else:
            return None

def 全流程(year, quarter):
    dict_has_get_all = 获取某季度财务分析数据(ct.CompanyProfitStatement,year, quarter)
    dict = 全量获取(year, quarter,dict_has_get_all)
    保存数据(dict, year, quarter)

def 获取_全量股票_公司利润表_某个季度(year,quarter):
    全流程(year, quarter)

# def 获取_全量股票_公司利润表_某个季度(year,quarter):
#
#     dirname = ct.GLOBAL_PATH + ct.SEPARATOR + ct.FUNDAMENTAL_DATA + ct.SEPARATOR + ct.CompanyProfitStatement + ct.SEPARATOR
#     filename = "%s-%s.xlsx" % (year, quarter)
#
#     writer = pd.ExcelWriter(dirname + filename)  # 产生保存文件
#     # 初始化全部股票代码
#     stockListInstance = StockDict()
#     # 对每个股票代码进行处理
#     count = 0
#     sleep_stock_num = 500
#     sleep_sec = 5
#
#     for element in stockListInstance.stockIdList:
#         if count == sleep_stock_num:
#             print('网页查询了%s个股票等待%s秒！' % (sleep_stock_num, sleep_sec))
#             time.sleep(sleep_sec)
#             count = 0
#         else:
#             count = count + 1
#
#         try:
#
#             print("开始获取%s股票的%s年%s季度的--公司利润表--数据。" % (element, year, quarter))
#
#             df = 获取_公司利润表(year, quarter, element)
#             if df is not None:
#                 df.to_excel(writer, sheet_name=element)
#                 # print(df)
#             else:
#                 print("%s无相关数据。" % element)
#
#         except:
#             print("获取%s失败################################################" % element)
#
#     writer.save()
#     writer.close()

if __name__ == '__main__':
    ##################################
    #  一般使用下面的函数
    ##################################

    # df = 获取_公司利润表(2010, 4, "000001")
    # print(df)
    # df = 全量获取(2010, 4)
    # print(df)
    # 全流程(2010, 4)

    获取_全量股票_公司利润表_某个季度(2020, 3)
    # 获取_全量股票_公司利润表_某个季度(2017, 3)
    #获取_全量股票_公司利润表_某个季度(2017, 2)
    #获取_全量股票_公司利润表_某个季度(2017, 1)

