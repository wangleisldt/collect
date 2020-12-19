# encoding:utf-8

import time

from urllib.request import urlopen, Request
import lxml.html
from lxml import etree
from pandas.compat import StringIO
import pandas as pd

from 函数目录 import profile as ct
from 数据采集.股票清单.股票清单获取 import StockDict


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
        #ct._write_head()
        df = _获取_公司利润表(year, quarter,stockId, 1, pd.DataFrame())
        if df is not None:
            return process_dataframe(df)
        else:
            return None



def _获取_公司利润表(year, quarter, stockId , pageNo, dataArr, retry_count=3, pause=0.001):
    #ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(ct.公司利润表_URL % (ct.P_TYPE['http'], stockId , year, 4 ))
            #print(ct.财务指标_URL % (ct.P_TYPE['http'], stockId , year, 4 ))
            text = urlopen(request, timeout=10).read()
            text = text.decode('GBK')
            text = text.replace('--', '无')
            #text = text.replace('--','' )
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table[@id='ProfitStatementNewTable0']/tbody/tr")
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>' % sarr
            df = pd.read_html(sarr)[0]
            return df
        except Exception as e:
            pass
            #print('获取财务数据出错。')
    #raise IOError(ct.NETWORK_URL_ERROR_MSG)

def 获取_全量股票_公司利润表_某个季度(year,quarter):

    dirname = ct.GLOBAL_PATH + ct.SEPARATOR + ct.FUNDAMENTAL_DATA + ct.SEPARATOR + ct.CompanyProfitStatement + ct.SEPARATOR
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

            print("开始获取%s股票的%s年%s季度的--公司利润表--数据。" % (element, year, quarter))

            df = 获取_公司利润表(year, quarter, element)
            if df is not None:
                df.to_excel(writer, sheet_name=element)
            else:
                print("%s无相关数据。" % element)

        except:
            print("获取%s失败################################################" % element)

    writer.save()
    writer.close()

if __name__ == '__main__':
    ##################################
    #  一般使用下面的函数
    ##################################


    获取_全量股票_公司利润表_某个季度(2010, 4)
    #获取_全量股票_公司利润表_某个季度(2017, 3)
    #获取_全量股票_公司利润表_某个季度(2017, 2)
    #获取_全量股票_公司利润表_某个季度(2017, 1)

