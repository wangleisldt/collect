from 函数目录 import profile as pf
from 函数目录.function import file_List_Func
from 数据采集.股票清单.股票清单获取 import StockDict
import pickle
import pandas as pd
from 函数目录.date import getYearMonthFromMonthLength


def 打开目录并拼接文件(dirname):

    # 打开根据年月打开目录读取里面的文件
    fileList = file_List_Func(dirname)
    df_list = []
    for filename in fileList:
        #df_dir[dirname + filename] = pd.read_excel(dirname + filename ,converters={1: str})
        df_list.append(pd.read_excel(dirname + filename ,converters={"股票代码": str}))

    for i in range(1,len(df_list)):
        if i == 1:
            df = pd.merge(df_list[i-1], df_list[i], on='股票代码')
        else:
            df = pd.merge(df, df_list[i], on='股票代码')

    df.to_excel('C:\\temp\\' + 'a' + pf.Execl)


if __name__ == '__main__':
    dirname = 'C:\\temp\\量化拼接\\'
    打开目录并拼接文件(dirname)