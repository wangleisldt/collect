from 函数目录 import profile as pf
from 函数目录.function import checkAndCreateDir
from 数据采集.股票清单.股票清单获取 import StockDict
import joblib
import pandas as pd
from 数据采集.标准类.采集标准类 import 采集标准类

def _根据参数产生url(market,stockid):
    if market == 0:
        market = 'SZ'
    else:
        market = 'SH'
    url = 'http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code={}{}'.format(market,stockid)
    #print(url)
    return url

def _获取股票清单和交易市场():
    stockid_market_list = StockDict().stock_id_market
    return stockid_market_list

def _保存企业类型(output_dict):
    base_dir_name = "%s%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA, pf.SEPARATOR)
    dir = base_dir_name + pf.财务分析 + pf.SEPARATOR
    checkAndCreateDir(dir)
    #filename_execl = "%s%s%s" % (base_dir_name, pf.企业类型 , pf.Execl)
    filename_gz = "%s%s%s" % (dir, pf.企业类型, pf.GZ)

    #print(output_dict)
    #df = pd.DataFrame(output_dict)
    #print(df)
    #df.to_excel(filename_execl)
    joblib.dump(output_dict, filename_gz, compress=3, protocol=None)

def 采集企业类型():
    stockid_market_list = _获取股票清单和交易市场()
    # print(stockid_market_list)
    print("开始获取数据：")
    output_dict = {}
    for element in stockid_market_list:
        stockid, market = element
        print("开始获取%s股票数据" % (stockid))
        instance = 采集标准类(url=_根据参数产生url(market,stockid))
        content = instance._获取数据()
        #print(content)
        #print(type(content))
        stock_type = _处理返回值(content)
        output_dict[stockid] = stock_type

    _保存企业类型(output_dict)

def _处理返回值(content):
    string_1 ='<input id="hidctype" type="hidden" value="'
    if content is not None:
        string_2 = content.split(string_1)
        #print(string_2[1])
        if len(string_2)  == 2:
            print("企业类型（财务报表使用）为： ",string_2[1][0])
        return string_2[1][0]
    else:
        return None

def 读取企业类型():
    base_dir_name = "%s%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA, pf.SEPARATOR)
    dir = base_dir_name + pf.财务分析 + pf.SEPARATOR
    filename_gz = "%s%s%s" % (dir, pf.企业类型, pf.GZ)

    return joblib.load(filename_gz, mmap_mode=None)

if __name__ == '__main__':
    采集企业类型()
    aa = 读取企业类型()
    for k,v in aa.items():
        print(k,v)