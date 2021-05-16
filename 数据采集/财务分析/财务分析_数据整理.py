# encoding:utf-8

import time
import numpy as np
import pandas as pd
from 函数目录 import function as fn
from 函数目录 import profile as pf

def 拼接需要处理的文件名(file_type, year_quarter):
    base_dir_name = "%s%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA, pf.SEPARATOR)
    filename = "%s%s%s%s%s" % (base_dir_name, file_type, pf.SEPARATOR, year_quarter, pf.Execl)
    return filename

def 拼接需要保存的文件名(file_type, year_quarter, suffix=pf.Execl):
    base_dir_name = "%s%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA, pf.SEPARATOR)
    dirname = "%s%s%s%s%s" % (base_dir_name, pf.AfterFinishingData, pf.SEPARATOR, file_type, pf.SEPARATOR)
    fn.checkAndCreateDir(dirname)
    filename = "%s%s%s" % (dirname, year_quarter, suffix)
    return filename

def 处理某个季度(year, quarter):
    file_type_list = [pf.FinancialIndex, pf.BalanceSheet, pf.CashFlowSheet, pf.CompanyProfitStatement]

    for e in file_type_list:
        filename = 拼接需要处理的文件名(e, year + "-" + quarter)
        dict_stock = 处理一个文件(filename)
        filename = 拼接需要保存的文件名(e, year + "-" + quarter, pf.Execl)
        dict_stock.to_excel(filename)
        # filename = 拼接需要保存的文件名(e, year + "-" + quarter, pf.PklFile)
        # fn.save_pkl_obj(dict_stock, filename)

#################################################
#  读取采集的文件，返回股票字典，股票的id为key
#################################################
def 处理一个文件(filename):
    print("开始读取 %s 文件。" % (filename))
    '''
   dict_df = pd.read_excel(filename, sheet_name=None)
    #return_dict = {}
    #for k, v in dict_df.items():
        #print(k)
        #dict_stock = v.set_index(0).T.to_dict('list')
        #return_dict[k] = dict_stock
        #return_dict[k] = v
    return dict_df 

    try:
        fileList = file_List_Func(dir_name)
        all_stock_dict = {}
        for filename in fileList:
            stockid1 ,year1, quarter1 = from_filename_get_info(filename)
            if quarter == quarter1:
                key = "%s-%s-%s" % (stockid1 ,year1, quarter1)
                fullfilename = "%s%s" % (dir_name,filename)
                print(fullfilename)
                df = pd.read_excel(fullfilename,usecols=[1,2])

                stock_list = np.array(df)       #通过将df转换成list然后再进行处理

                one_stock_dict = {}
                for element in stock_list:      #对list的每一行进行处理
                    one_stock_dict[element[0]] = element[1]
                all_stock_dict[key] = one_stock_dict
        return all_stock_dict
    except:
        print("文件 %s 有问题。请将其删除重新采集。" % (fullfilename))
        raise Exception("文件 %s 有问题。请将其删除重新采集。" % (fullfilename))
    '''

    # dict_df = pd.read_excel(filename, sheet_name=None)
    dict_df = pd.read_excel(filename, sheet_name=None,index_col = 0)
    output_df = pd.DataFrame()  # 生成要输出的dataframe
    for stock_id, df in dict_df.items():
        if df.empty :
            pass
        else:
            df1 = pd.DataFrame({'类型': ['股票代码'], '值': [stock_id]})  # 增加股票代码
            # print(stock_id)
            # print(df)
            df.columns = ['类型', '值']  # 将dataframe的列改名
            df.iloc[0, 0] = '报告日期'  # 修改一些值，如报告日期
            # df.iloc[0, 1] = df.iloc[0, 1][0:7]#修改一些值，将原来2018-03-31修改为2018-03，代表一季度
            # print(df)
            df = pd.concat([df1, df])  # 将股票代码和读取的dataframe进行合并

            df.drop_duplicates('类型', keep='first', inplace=True)  # 根据类型对重复的行进行删除

            df = df.set_index(['类型'])  # 将股票的指标类型设在为索引
            # print(df)

            output_df = pd.concat([output_df, df.T])  # 由于这是每个文件记录是竖排的，所以需要将其倒置，并进行合并


    # 将股票代码和日期放到第一列
    # get a list of columns
    cols = list(output_df)
    # move the column to head of list using index, pop and insert
    cols.insert(0, cols.pop(cols.index('股票代码')))
    cols.insert(1, cols.pop(cols.index('报告日期')))
    # use ix to reorder
    # print(output_df)
    # output_df = output_df.ix[:, cols]
    output_df = output_df.loc[:, cols]

    output_df = output_df.reset_index(drop=True)  # 由于倒置的时候，将索引都设置为了‘值’，所以需要对索引进行重置排序

    return output_df

if __name__ == '__main__':
    处理某个季度('2020', '4')
