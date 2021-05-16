import pandas as pd
import numpy as np

from 函数目录 import profile as pf
from 函数目录.date import get_1_quarter_after
from 数据采集.股票清单.股票清单获取 import StockDict
from 数据采集.标准类.采集标准类 import 采集标准类
import json
from 函数目录.function import checkAndCreateDir
import joblib
from 函数目录.function import check_file_exist

机构持股列名 = ['日期', '机构属性', '持股家数(家)', '持股总数', '持股市值', '占总股本比例(%)', '占流通股比例(%)']

base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
dirname = "%s%s%s%s%s" % (base_dir_name, pf.SEPARATOR, pf.机构持股目录, pf.SEPARATOR, pf.步骤一)
full_dir_name = f"{dirname}{pf.SEPARATOR}"


def 单个股票进行获取(year, quarter,stockid,market, end_date):

    instance = 采集标准类(url=_根据参数产生url(stockid, market, end_date))
    return_list = instance._获取数据_json()
    #print(return_list)
    return _处理返回值(return_list)

def 根据全量股票进行获取(year, quarter):
    end_date = _将年季度转换为本季度末日期(year, quarter)
    stockid_market_list = _获取股票清单和交易市场()

    dict_df = 读取机构持股目录步骤一文件(year, quarter)

    #print(stockid_market_list)
    print(end_date)
    print("开始获取数据：")
    return_dict = {}

    for element in stockid_market_list:
        stockid, market = element
        print("开始获取%s股票数据" % (stockid))
        if stockid in dict_df.keys():
            return_dict[stockid] = dict_df[stockid]
            print("该股票已采集过@@@@")
            # print(dict_df[stockid])
        else:
            # print(year, quarter, stockid, market, end_date)
            df_one_stock = 单个股票进行获取(year, quarter, stockid, market, end_date)
            if df_one_stock is not None:
                return_dict[stockid] = df_one_stock
                print("采集了数据********************************")
                # print(return_dict[stockid])
            else:
                print("该股票无数据+++++++++++++")

    保存采集到的机构持股数据(return_dict,year ,quarter)


def _获取股票清单和交易市场():
    stockid_market_list = StockDict().stock_id_market_sh_sz
    return stockid_market_list

def _根据参数产生url(stockid,market,end_date):
    url = 'http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/GGZLSJTJ/GetGGZLSJTJ?tkn=eastmoney&reportDate={}&code={}.{}&cfg=ggzlsjtj'.format(end_date,stockid,market )
    # print(url)
    return url

def _处理返回值(dict):
    try:
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
                    # print("机构持股为0")
                    return None
                else:
                    return df
        else:
            print("采集不到机构持股数据")
            return None
    except:
        print("处理返回值时失败。**************************")
        return None

def _将年季度转换为本季度末日期(year ,quarter):
    quarter = pf.End_OF_SEASON_DAY[quarter]
    return str(year)+quarter

def 读取机构持股目录步骤一文件(year ,quarter):
    filename = f"{year}-{quarter}{pf.GZ}"
    if check_file_exist(full_dir_name,filename):
        print("存在之前采集数据，正在进行读取。")
        full_file_name = f"{full_dir_name}{filename}"
        print(full_file_name)
        df_file = joblib.load(full_file_name, mmap_mode=None)
        return df_file
    else:
        print("不存在之前采集数据")
        return {}

def 保存采集到的机构持股数据(dict_df,year ,quarter):
    filename = f"{year}-{quarter}{pf.GZ}"
    full_file_name = f"{full_dir_name}{filename}"
    print(f"开始保存数据到：{full_file_name}")
    joblib.dump(dict_df, full_file_name, compress=3, protocol=None)

def 从文件获取机构持股数据(year ,quarter):
    filename = f"{year}-{quarter}{pf.GZ}"
    full_file_name = f"{full_dir_name}{filename}"
    print(f"开始读取{full_file_name}")
    return joblib.load(full_file_name, mmap_mode=None)

def 按年获取数据(year):
    根据全量股票进行获取(year, 1)
    根据全量股票进行获取(year, 2)
    根据全量股票进行获取(year, 3)
    根据全量股票进行获取(year, 4)

if __name__ == '__main__':
    根据全量股票进行获取(2021, 1)

    # df = 单个股票进行获取(2020, 1, '002112' ,'SZ','2020-03-31')
    # print(df)

    # dict = 从文件获取机构持股数据(2020, 1)
    # for k,v in dict.items():
    #     print(k)
    #     print(v)

    # 按年获取数据(2020)
    # 按年获取数据(2019)
    # 按年获取数据(2018)
    # 按年获取数据(2017)
    # 按年获取数据(2016)
    # 按年获取数据(2015)
    # 按年获取数据(2014)
    # 按年获取数据(2013)
    # 按年获取数据(2012)
    # 按年获取数据(2011)
    # 按年获取数据(2010)
