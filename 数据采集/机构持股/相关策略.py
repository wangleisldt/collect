from 数据采集.机构持股.获取指定数据 import 获取指定季度前几个月的数据,获取机构持股指定数据
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import get_1_quarter_before
import pandas as pd
from 函数目录 import profile as pf

def 获取机构汇总数据到字典(dict,stockid,year,quarter ,num ,col ,type='机构汇总'):
    output_dict = {}
    for i in range(0,num):
        output = 获取机构持股指定数据(dict, stockid, year,quarter, type, col)
        # print(output)
        output_dict[ f'{col}-{year}-{quarter}'] = output
        year, quarter = get_1_quarter_before(year, quarter)

    return output_dict

def 计算增长(dict,year,quarter ,num,col):
    output_dict = {}
    for i in range(0,num-1):
        year_before, quarter_before = get_1_quarter_before(year, quarter)
        # 当前季度 = dict[f'{year}-{quarter}-持股家数(家)']
        # 前一季度 = dict[f'{year_before}-{quarter_before}-持股家数(家)']
        output_dict[f'季度增长@{year}-{quarter}-{col}'] = dict[ f'{col}-{year}-{quarter}'] - dict[ f'{col}-{year_before}-{quarter_before}']
        year, quarter = get_1_quarter_before(year, quarter)

    return output_dict

def 策略(year,quarter ,num):
    dict = 获取指定季度前几个月的数据(year,quarter ,num)
    print("开始处理：")
    output_list = []
    stock_instance = StockDict()
    for element in stock_instance.stockIdList:
        output_dict = {}
        output_dict['股票代码'] = element
        output_dict['股票名称'] = stock_instance.stockDict[pf.股票清单表头[1]][element]

        # 持股家数处理
        col_name = '持股家数(家)'
        return_dict = 获取机构汇总数据到字典(dict, element, year, quarter, num,col=col_name ,type='机构汇总' )
        output_dict.update(return_dict)
        d = 计算增长(return_dict, year, quarter, num,col=col_name)
        output_dict.update(d)

        # 占总股本比例(%)
        col_name = '占总股本比例(%)'
        return_dict = 获取机构汇总数据到字典(dict, element, year, quarter, num, col=col_name, type='机构汇总')
        output_dict.update(return_dict)
        d = 计算增长(return_dict, year, quarter, num, col=col_name)
        output_dict.update(d)

        output_list.append(output_dict)

    pd.set_option('display.width', 1000)
    pd.set_option('max_colwidth', 10)
    df = pd.DataFrame.from_dict(output_list)
    df.set_index(['股票代码','股票名称'], inplace=True)
    print(df)

    return df

def 根据策略产生数据(year,quarter ,num):
    df = 策略(year , quarter , num)
    base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
    dirname = "%s%s%s%s" % (base_dir_name, pf.SEPARATOR, pf.机构持股目录, pf.SEPARATOR)
    full_dir_name = f"{dirname}"
    full_filename = f"{full_dir_name}机构持股数据结果.xlsx"
    print(full_filename)
    df.to_excel(full_filename)

if __name__ == '__main__':
    根据策略产生数据(2021, 1, 2)