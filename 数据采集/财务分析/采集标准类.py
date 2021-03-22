# encoding:utf-8

import time
# import requests
from lxml import etree
import pandas as pd
from 函数目录 import profile as ct
from 数据采集.标准类.采集标准类 import 采集标准类
# from 函数目录 import date
# from 函数目录.function import save_file_dataframe_to_execl
# from 数据采集.股票清单.股票清单获取 import StockDict
# from 函数目录.function import check_file_exist

# def new_获取_现金流量表():
#     # ct._write_console()
#     # for _ in range(retry_count):
#     #     time.sleep(pause)
#     try:
#         # 访问网站的标准三步
#         url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/000001/ctrl/2020/displaytype/4.phtml'
#         text = requests.get(url).text
#         html = etree.HTML(text)
#         # 定位指定表格
#         res = html.xpath("//table[@id='BalanceSheetNewTable0']/tbody/tr")
#         # 将表格数据转换为一个list
#         sarr = [etree.tostring(node).decode('utf-8') for node in res]
#         # 在list前后增加table属性
#         sarr = '<table>%s</table>' % sarr
#         # 使用pandas的readhtml模块读取表格
#         # 其实也是可以直接使用readhtml模块进行读取表格，但是会有多个表格，
#         # 这个程序只是对表格先期进行了一个筛选。
#         df = pd.read_html(sarr)
#         print(df)
#         return df
#     except Exception as e:
#         print('获取财务数据出错。')
#     #raise IOError(ct.NETWORK_URL_ERROR_MSG)

def 获取_财务分析表(url_input ,year, quarter, stockId , pageNo, dataArr, table_xpath , retry_count=3, pause=0.001  ):
    #ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            url = url_input % (ct.P_TYPE['http'], stockId, year, 4)
            instance = 采集标准类(url=url)
            # print(url)
            text = instance._获取数据_text()
            text = text.replace('--', '无')
            # text = requests.get(url).text
            html = etree.HTML(text)
            # 定位指定表格
            # res = html.xpath("//table[@id='BalanceSheetNewTable0']/tbody/tr")
            res = html.xpath(table_xpath)
            # 将表格数据转换为一个list
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
            # 在list前后增加table属性
            sarr = '<table>%s</table>' % sarr
            # 使用pandas的readhtml模块读取表格
            # 其实也是可以直接使用readhtml模块进行读取表格，但是会有多个表格，
            # 这个程序只是对表格先期进行了一个筛选。
            df = pd.read_html(sarr)[0]
            # print(df)
            return df
        except Exception as e:
            pass
        #     print('获取数据出错。')
        # raise IOError(ct.NETWORK_URL_ERROR_MSG)

# def _获取_公司利润表_old(year, quarter, stockId , pageNo, dataArr, retry_count=3, pause=0.001):
#     #ct._write_console()
#     for _ in range(retry_count):
#         time.sleep(pause)
#         try:
#             # request = Request(ct.公司利润表_URL % (ct.P_TYPE['http'], stockId , year, 4 ))
#             # #print(ct.财务指标_URL % (ct.P_TYPE['http'], stockId , year, 4 ))
#             # text = urlopen(request, timeout=10).read()
#             # text = text.decode('GBK')
#             # text = text.replace('--', '无')
#             # #text = text.replace('--','' )
#             # html = lxml.html.parse(StringIO(text))
#             # res = html.xpath("//table[@id='ProfitStatementNewTable0']/tbody/tr")
#             # sarr = [etree.tostring(node).decode('utf-8') for node in res]
#             # sarr = ''.join(sarr)
#             # sarr = '<table>%s</table>' % sarr
#             # df = pd.read_html(sarr)[0]
#             # print(df)
#             return df
#         except Exception as e:
#             pass
#             #print('获取财务数据出错。')
#     #raise IOError(ct.NETWORK_URL_ERROR_MSG)

if __name__ == '__main__':
    pass

    # new_获取_现金流量表()
