import pandas as pd
from 函数目录 import profile as pf
from 函数目录.function import checkAndCreateDir
import joblib
from 数据采集.机构持股.机构持股采集 import 从文件获取机构持股数据

base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
dirname_步骤二 = "%s%s%s%s%s" % (base_dir_name, pf.SEPARATOR, pf.机构持股目录, pf.SEPARATOR, pf.步骤二)
full_dir_name = f"{dirname_步骤二}{pf.SEPARATOR}"

def 保存汇总机构持股数据(df,year ,quarter):
    filename = f"{year}-{quarter}{pf.GZ}"
    full_file_name = f"{full_dir_name}{filename}"
    print(f"开始保存数据到：{full_file_name}")
    checkAndCreateDir(full_dir_name)
    joblib.dump(df, full_file_name, compress=3, protocol=None)

def 数据整理(year ,quarter):
    dict = 从文件获取机构持股数据(year ,quarter)
    key = f'{year}-{quarter}'
    output_dict ={}
    output_dict[key] = dict
    保存汇总机构持股数据(output_dict, year, quarter)

# def 数据整理(year ,quarter):
#     dict = 从文件获取机构持股数据(year ,quarter)
#     output_df = pd.DataFrame()
#     for stock_id, df in dict.items():
#         df['股票代码'] = stock_id
#         # print(df)
#         output_df = output_df.append(df)
#     # output_df.set_index('股票代码', inplace=True)
#     # print(output_df)
#     保存汇总机构持股数据(output_df, year, quarter)

def 从文件获取机构持股数据步骤二(year ,quarter):
    filename = f"{year}-{quarter}{pf.GZ}"
    full_file_name = f"{full_dir_name}{filename}"
    print(f"开始读取{full_file_name}")
    return joblib.load(full_file_name, mmap_mode=None)

if __name__ == '__main__':

    数据整理(2020, 3)
    数据整理(2020, 2)
    数据整理(2020, 1)
    # df = 从文件获取机构持股数据(2020, 2)
    # print(df)
    # df[df["机构属性"] == '机构汇总']

    # df = 从文件获取机构持股数据步骤二(2020, 2)
    # print(df)


