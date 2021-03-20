# encoding:utf-8

'''
第一数字定律——Benford's law——数字舞弊识别方法
第一位有效数字     1       2        3        4       5       6         7        8       9
根据本福德法则计算的结果     30.1%  17.6%  12.5%   9.7%    7.9%    6.7%    5.8%    5.1%    4.6%

{1 :301 , 2: 176 ,3: 125  ,4: 97   ,5: 79  ,6:  67   ,7: 58  ,8:  51   ,9: 46}
'''

from 函数目录.function import checkAndCreateDir
from 函数目录.function import file_List_Func
from 函数目录.function import from_filename_get_info
from 函数目录 import profile as pf
import 函数目录.CalculateFuncation as cal
import pandas as pd
import numpy as np
import pickle
from collections import Counter

def addTwoDicTogether(x,y):
    X, Y = Counter(x), Counter(y)
    return dict(X + Y)


def returnDictSum(myDict):
    sum = 0
    for i in myDict:
        sum = sum + myDict[i]
    return sum

def 读取某个文件(filename):
    df = pd.read_excel(filename, converters={0: str})
    df.fillna(0,inplace=True)
    df.replace('无', 0,inplace=True)
    df.drop('报告日期',axis=1,inplace=True)
    return_list = df.values.tolist()
    #print(df)
    return return_list

def 拆分list统计字符串(df_list):

    for e in df_list:
        dict_count_one_stock = {}
        dict_count_one_stock1 = {}
        #print(e[0])
        for i in range(1,len(e)):
            #dict_count = 统计字符串每个数字出现的频率(str(e[i]))
            dict_首字母 = 统计字符串第一个非零数字出现的频率(str(e[i]))
            #print(e[i])
            #dict_count_one_stock = addTwoDicTogether(dict_count_one_stock, dict_count)
            dict_count_one_stock1 = addTwoDicTogether(dict_count_one_stock1, dict_首字母)

        sum_value = returnDictSum(dict_count_one_stock1)

        for k,v in dict_count_one_stock1.items():
            dict_count_one_stock1[k] = int(v/sum_value*100)

        #print(dict_count_one_stock)

        arr = sorted(dict_count_one_stock1.items(),key = lambda item:item[0])
        #print(dict_count_one_stock1)
        #print(arr)
        print(e[0],计算偏差(dict_count_one_stock1))


def 统计字符串每个数字出现的频率(string):
    string_list = list(string)
    #print(string)
    c = dict()
    for i in string_list:
        if i != '-' and i != '0' and i != '.' :
            if i in c:
                c[i] += 1
            else:
                c[i] = 1
    return c


def 统计字符串第一个非零数字出现的频率(string):
    string_list = list(string)
    c = dict()
    for i in string_list:
        if i not in ['0', '.' , '-']:
            c[i] = 1
            return c
    return c

def 计算偏差(dict):
    one_dict = {1: 301, 2: 176, 3: 125, 4: 97, 5: 79, 6: 67, 7: 58, 8: 51, 9: 46}
    one_dict = {1: 30, 2: 17, 3: 12, 4: 9, 5: 7, 6: 6, 7: 5, 8: 5, 9: 4}
    result_list = []

    for i in range(1,4):
        if str(i) in dict.keys():
            #result_list.append(dict[str(i)] - one_dict[i])
            result_list.append(cal.calListStdev(  [  dict[str(i)] , one_dict[i]   ] ))

    #return int(np.var(result_list)),int(np.std(result_list,ddof=1))
    #print(result_list)
    return sum(result_list)
#sdfsdf
#sdfsd


if __name__ == '__main__':
    df_list = 读取某个文件('C:\\量化\\基本面数据\\整理后的数据目录\\财务指标\\2019-2.xlsx')
    拆分list统计字符串(df_list)
