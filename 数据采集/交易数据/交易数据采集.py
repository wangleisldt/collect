import requests
import json
import chardet
import pandas as pd
import time
import pickle
import os,shutil
from 函数目录 import profile as pf
from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getCurrentDate
from 数据采集.标准类.采集标准类 import 请求数据_原始,采集标准类
from 数据采集.交易数据.交易数据保存 import 保存交易数据

#原始url为：
#http://87.push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.002507&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=1000000

def 根据全量股票进行获取(fqt='2', day_limit='9999999999999'):
    # fqt  为 2 时，后复权
    # fqt 为 1 时，前复权
    # fqt 为 0 时，不复权
    stockid_market_list = _获取股票清单和交易市场()
    # print(stockid_market_list)
    print("开始获取交易数据：")
    for element in stockid_market_list:
        stockid, market = element
        print("开始获取%s股票交易数据" % (stockid))
        instance = 采集标准类(url = _根据参数产生url(market, stockid, fqt=fqt, day_limit=day_limit))
        list = instance._获取数据_json()
        df = _处理返回值(list)
        if df is not None:
            print("开始保存股票列表")
            保存交易数据(stockid,df)
            #print("结束保存股票列表")
        else:
            print("无交易数据")

def _获取股票清单和交易市场():
    stockid_market_list = StockDict().stock_id_market
    return stockid_market_list

def _根据参数产生url(market,stockid ,fqt,day_limit):
    url = 'http://87.push2his.eastmoney.com/api/qt/stock/kline/get?secid={}.{}&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt={}&end=20500101&lmt={}'.format(market,stockid ,fqt,day_limit)
    return url

def _处理返回值(list):
    stock_transactional_list = list["data"]["klines"]
    for i in range(len(stock_transactional_list)):
        stock_transactional_list[i] = stock_transactional_list[i].split(",")
    if len(stock_transactional_list) != 0:
        df = pd.DataFrame(stock_transactional_list)
        #print(df)
        df.columns = pf.股票日交易表头
        #print(df)
    else:
        df = None
    return df

if __name__ == '__main__':
    根据全量股票进行获取(day_limit='98888888889')

