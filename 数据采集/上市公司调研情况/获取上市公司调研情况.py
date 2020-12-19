import requests
import json

import chardet

import pandas as pd

import time

import pickle

import os

from 函数目录 import profile as pf

from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getCurrentDate

class 获取上市公司调研情况_根据股票代码一个一个获取():
    # 初始化
    def __init__(self):
        self.count = 300 #查询多少个股票后，等待一下
        self.wait_sec = 5 #等待时间

        self.output_list = []

        self.columns = ['股票代码', '股票名称', '调研次数','调研时间', '公告日期', '接待方式']

    def 根据全量股票进行获取(self):
        # 检查要保存的目录是否存在
        base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        dirname = "%s%s%s%s%s%s" % (
            base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据 ,pf.SEPARATOR)
        checkAndCreateDir(dirname)

        writer = pd.ExcelWriter(dirname + pf.投资者关系活动记录表 +  getCurrentDate() +pf.Execl)  # 产生保存文件

        #初始化全部股票代码
        stockListInstance = StockDict()
        #对每个股票代码进行处理
        count = 0
        for element in stockListInstance.stockIdList:
            if count == self.count:
                print("网页查询了%s个股票等待%s秒！" %  (self.count,self.wait_sec))
                time.sleep(self.wait_sec)
                count = 0
            else:
                count = count + 1

            try:
                print("开始获取%s" % (element))
                df = self.获取数据(element)
                #print(df)

                if df is not None:
                    df.to_excel(writer, sheet_name=element)
                else:
                    print("%s无相关数据。" % element)
            except:
                print("获取%s失败################################################"  %element )

        writer.save()
        writer.close()

        #下面部分对文件进行合并
        base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        dirname = "%s%s%s%s%s%s" % (
            base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR)

        dict_df_之前数据 = pd.read_excel(dirname + pf.投资者关系活动记录表 + pf.Execl, sheet_name=None,
                                    converters={0: str})  # 将其转换为字符串，这样就比较好处理

        dict_df_今天数据 = pd.read_excel(dirname + pf.投资者关系活动记录表 + getCurrentDate() + pf.Execl, sheet_name=None,
                                     converters={0: str})  # 将其转换为字符串，这样就比较好处理

        for stockid_new, df_new in dict_df_今天数据.items():
            if stockid_new in dict_df_之前数据.keys():
                dict_df_之前数据[stockid_new] = pd.concat([dict_df_之前数据[stockid_new], df_new]).drop_duplicates(inplace=False).sort_values(by=['调研时间'],ascending = False).reset_index(drop=True)
            else:
                dict_df_之前数据[stockid_new] = df_new

        writer = pd.ExcelWriter(dirname + pf.投资者关系活动记录表  + pf.Execl)  # 产生保存文件
        for e in sorted(dict_df_之前数据.keys()):
            dict_df_之前数据[e].to_excel(writer, sheet_name=e)
        writer.save()
        writer.close()



    def 获取数据(self, stockid):
        """
            获取东方财富网投资者活动关系
            :param stockid: string e.g. 000860
            :param pause:
            :return:
            """

        def 处理返回字典将其转换为List(dict):
            returnList = []
            for element in dict['data']:
                list = []
                list.append(element['SCode'])
                list.append(element['SName'])
                list.append(element['OrgSum'])
                list.append(element['StartDate'])
                list.append(element['NoticeDate'])
                list.append(element['Description'])
                returnList.append(list)

            # 对第几列进行排序，现在是第4列
            def sort_col(elem):
                return elem[3]

            returnList.sort(key=sort_col, reverse=True)
            return returnList

        url = "http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=50&page=1&js=var%%20eKYgfdmv&param=&sortRule=-1&sortType=0&code=%s&name=%%25E6%%25B6%%25AA%%25E9%%2599%%25B5%%25E6%%25A6%%25A8%%25E8%%258F%%259C&rt=51230292" % (stockid)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }

        response = requests.post(url,headers=headers)

        fencoding = chardet.detect(response.content)

        content = response.content.decode(fencoding['encoding'],errors = 'ignore')[13:]

        #print(content)
        dict = json.loads(content)
        list = 处理返回字典将其转换为List(dict)

        if len(list) != 0:
            df = pd.DataFrame(list, columns=self.columns)
            #for e in list:
                #print(e)
            return df
        else:
            return None


if __name__ == '__main__':
    a = 获取上市公司调研情况_根据股票代码一个一个获取()
    a.根据全量股票进行获取()

