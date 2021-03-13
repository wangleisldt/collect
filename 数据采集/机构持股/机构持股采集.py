import pandas as pd
import numpy as np

from 函数目录 import profile as pf
from 函数目录.date import get_1_quarter_after
from 数据采集.股票清单.股票清单获取 import StockDict
from 数据采集.标准类.采集标准类 import 采集标准类
from 数据采集.三张报表.采集企业类型 import 读取企业类型,采集企业类型
import json
from 函数目录.function import checkAndCreateDir
import joblib

机构持股列名 = ['日期', '机构属性', '持股家数(家)', '持股总数', '持股市值', '占总股本比例(%)', '占流通股比例(%)']

def 单个股票进行获取(year, quarter,stockid,market, end_date):
    print("开始获取%s股票数据" % (stockid))
    instance = 采集标准类(url=_根据参数产生url(stockid, market, end_date))
    return_list = instance._获取数据_json()
    #print(return_list)
    return _处理返回值(return_list)

def 根据全量股票进行获取(year, quarter):
    end_date = _将年季度转换为本季度末日期(year, quarter)
    stockid_market_list = _获取股票清单和交易市场()

    #print(stockid_market_list)
    print(end_date)
    print("开始获取数据：")
    return_dict = {}

    for element in stockid_market_list:
        stockid, market = element
        return_df = 单个股票进行获取(year, quarter, stockid, market, end_date)
        #print(return_df)

def _获取股票清单和交易市场():
    stockid_market_list = StockDict().stock_id_market_sh_sz
    return stockid_market_list

def _根据参数产生url(stockid,market,end_date):
    url = 'http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/GGZLSJTJ/GetGGZLSJTJ?tkn=eastmoney&reportDate={}&code={}.{}&cfg=ggzlsjtj'.format(end_date,stockid,market )
    #print(url)
    return url

def _处理返回值(dict):
    if dict is not None:
        #print(dict['Data'])
        for e in dict['Data']:
            #print(e)
            split_symbol = e['SplitSymbol']
            list = e['Data']
            list_tmp = []
            for element in list:
                #print(element)
                line_list = element.split(split_symbol)
                for i in range(len(line_list)):
                    if line_list[i] == '':
                        line_list[i] = 0
                list_tmp.append(line_list)
            df = pd.DataFrame(data= list_tmp)

            #df[0] = df[0].astype(object)
            #df[1] = df[1].astype(object)
            df[2] = df[2].astype(int)
            df[3] = df[3].astype(int)
            df[4] = df[4].astype(float)
            df[5] = df[5].astype(float)
            df[6] = df[6].astype(float)

            df.columns = 机构持股列名
            #print(df)
            持股家数 =df.loc[6, 机构持股列名[2]]
            if 持股家数 == 0:
                print("机构持股为0")
                return None
            else:
                return df
    else:
        print("采集不到机构持股数据")
        return None

def _将年季度转换为本季度末日期(year ,quarter):
    quarter = pf.End_OF_SEASON_DAY[quarter]
    return str(year)+quarter

if __name__ == '__main__':
    根据全量股票进行获取(2020, 1)