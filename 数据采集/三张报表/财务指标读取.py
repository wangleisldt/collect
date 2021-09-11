# import pandas as pd
from 函数目录 import profile as pf
# from 函数目录.date import get_1_quarter_after
# from 数据采集.股票清单.股票清单获取 import StockDict
# from 数据采集.标准类.采集标准类 import 采集标准类
# from 数据采集.三张报表.采集企业类型 import 读取企业类型,采集企业类型
# import json
# from 函数目录.function import checkAndCreateDir
import joblib
from pathlib import Path

def 财务指标读取(type,date):
    p = Path(pf.GLOBAL_PATH, pf.FUNDAMENTAL_DATA, pf.财务分析)
    filename_gz = Path(p  , f'{type}{date}{pf.GZ}')

    # base_dir_name = "%s%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA, pf.SEPARATOR)
    # dir = base_dir_name + pf.财务分析 + pf.SEPARATOR
    # filename_gz = "%s%s%s%s" % (dir, type,date , pf.GZ)

    print(f'开始读取 {filename_gz}')

    return joblib.load(filename_gz, mmap_mode=None)

if __name__ == '__main__':
    aa = 财务指标读取('主要指标',20201)
    #aa = 财务指标读取('资产负债表', 20203)
    #aa = 财务指标读取('现金流量表', 20203)
    #aa = 财务指标读取('利润表', 20203)
    for k,v in aa.items():
        print(k)

        for key,val in v.items():
            print(key,'---------',val)
