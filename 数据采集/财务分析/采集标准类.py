# encoding:utf-8

# 还在开发未上线
import time
import requests
from lxml import etree
import pandas as pd
# from 函数目录 import profile as ct
# from 函数目录 import date
# from 函数目录.function import save_file_dataframe_to_execl
# from 数据采集.股票清单.股票清单获取 import StockDict
# from 函数目录.function import check_file_exist

def new_获取_现金流量表():
    # ct._write_console()
    # for _ in range(retry_count):
    #     time.sleep(pause)
    try:
        # 访问网站的标准三步
        url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/000001/ctrl/2020/displaytype/4.phtml'
        text = requests.get(url).text
        html = etree.HTML(text)
        # 定位指定表格
        res = html.xpath("//table[@id='BalanceSheetNewTable0']/tbody/tr")
        # 将表格数据转换为一个list
        sarr = [etree.tostring(node).decode('utf-8') for node in res]
        # 在list前后增加table属性
        sarr = '<table>%s</table>' % sarr
        # 使用pandas的readhtml模块读取表格
        # 其实也是可以直接使用readhtml模块进行读取表格，但是会有多个表格，
        # 这个程序只是对表格先期进行了一个筛选。
        df = pd.read_html(sarr)
        print(df)
        return df
    except Exception as e:
        print('获取财务数据出错。')
    #raise IOError(ct.NETWORK_URL_ERROR_MSG)

if __name__ == '__main__':

    new_获取_现金流量表()
