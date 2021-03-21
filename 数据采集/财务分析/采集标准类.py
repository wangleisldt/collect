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
        url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/000001/ctrl/2020/displaytype/4.phtml'
        text = requests.get(url).text
        html = etree.HTML(text)
        res = html.xpath("//table[@id='BalanceSheetNewTable0']/tbody/tr")
        sarr = [etree.tostring(node).decode('utf-8') for node in res]
        sarr = '<table>%s</table>' % sarr
        df = pd.read_html(sarr)
        print(df)
        return df
    except Exception as e:
        print('获取财务数据出错。')
    #raise IOError(ct.NETWORK_URL_ERROR_MSG)

if __name__ == '__main__':

    new_获取_现金流量表()

