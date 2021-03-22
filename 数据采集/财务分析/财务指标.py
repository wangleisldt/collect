# encoding:utf-8

import time

# from urllib.request import urlopen, Request
# import lxml.html
# from lxml import etree
# from pandas.compat import StringIO
import pandas as pd

from 函数目录 import profile as ct

# from 函数目录 import date
#
# from 函数目录.function import save_file_dataframe_to_execl

from 数据采集.股票清单.股票清单获取 import StockDict

# from 函数目录.function import check_file_exist
from 数据采集.财务分析.采集标准类 import 获取_财务分析表

URL = ct.财务指标_URL
TABLE_XPATH = "//table[@id='BalanceSheetNewTable0']/tbody/tr"

def 获取_财务指标(year, quarter ,stockId):
    """
        获取业绩报表数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
       说明：由于是从网站获取的数据，需要一页页抓取，速度取决于您当前网络速度

    Return
    --------
    DataFrame
        code,代码
        name,名称
        eps,每股收益
        eps_yoy,每股收益同比(%)
        bvps,每股净资产
        roe,净资产收益率(%)
        epcf,每股现金流量(元)
        net_profits,净利润(万元)
        profits_yoy,净利润同比(%)
        distrib,分配方案
        report_date,发布日期
    """
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
        #ct._write_head()
        df = 获取_财务分析表(URL, year, quarter, stockId, 1, pd.DataFrame(), TABLE_XPATH)
        # df = _获取_财务指标(year, quarter,stockId, 1, pd.DataFrame())
        if df is not None:
            return process_dataframe(df)
        else:
            return None


#
# def _获取_财务指标(year, quarter, stockId , pageNo, dataArr, retry_count=3, pause=0.001):
#     #ct._write_console()
#     for _ in range(retry_count):
#         time.sleep(pause)
#         try:
#             request = Request(ct.财务指标_URL % (ct.P_TYPE['http'], stockId , year, 4 ))
#             #print(ct.财务指标_URL % (ct.P_TYPE['http'], stockId , year, 4 ))
#             text = urlopen(request, timeout=10).read()
#             text = text.decode('GBK')
#             text = text.replace('--', '无')
#             #text = text.replace('--','' )
#             html = lxml.html.parse(StringIO(text))
#             res = html.xpath("//table[@id='BalanceSheetNewTable0']/tbody/tr")
#             sarr = [etree.tostring(node).decode('utf-8') for node in res]
#             sarr = ''.join(sarr)
#             sarr = '<table>%s</table>' % sarr
#             df = pd.read_html(sarr)[0]
#             return df
#         except Exception as e:
#             pass
#             #print('获取财务数据出错。')
#     #raise IOError(ct.NETWORK_URL_ERROR_MSG)



def 获取_全量股票_财务指标_某个季度(year,quarter):

    dirname = ct.GLOBAL_PATH + ct.SEPARATOR + ct.FUNDAMENTAL_DATA + ct.SEPARATOR + ct.FinancialIndex + ct.SEPARATOR

    filename = "%s-%s.xlsx" % (year, quarter)

    writer = pd.ExcelWriter(dirname + filename)  # 产生保存文件
    # 初始化全部股票代码
    stockListInstance = StockDict()
    # 对每个股票代码进行处理
    count = 0
    sleep_stock_num = 500
    sleep_sec = 5

    for element in stockListInstance.stockIdList:
        if count == sleep_stock_num:
            print('网页查询了%s个股票等待%s秒！' % (sleep_stock_num, sleep_sec))
            time.sleep(sleep_sec)
            count = 0
        else:
            count = count + 1

        try:

            print("开始获取%s股票的%s年%s季度的--财务指标--数据。" % (element, year, quarter))

            df = 获取_财务指标(year, quarter, element)
            if df is not None:
                df.to_excel(writer, sheet_name=element)
            else:
                print("%s无相关数据。" % element)

        except:
            print("获取%s失败################################################" % element)

    writer.save()
    writer.close()



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

    获取_全量股票_财务指标_某个季度(2017,2)

