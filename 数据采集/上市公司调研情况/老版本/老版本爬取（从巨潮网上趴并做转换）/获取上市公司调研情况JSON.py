import requests
import json

import chardet

import pandas as pd

import pickle

import os

from 函数目录 import profile as pf

from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict


class 获取上市公司调研情况_根据股票代码一个一个获取():
    # 初始化
    def __init__(self):
        pass

    def 根据全量股票进行获取(self):
        # 检查要保存的目录是否存在
        base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        dirname = "%s%s%s%s%s%s" % (
            base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR)
        checkAndCreateDir(dirname)

        #初始化全部股票代码
        stockListInstance = StockDict()
        #对每个股票代码进行处理
        for element in stockListInstance.stockIdList:
            self.获取数据(element)

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

        response = requests.post(url)

        fencoding = chardet.detect(response.content)

        content = response.content.decode(fencoding['encoding'],errors = 'ignore')[13:]

        #print(content)
        dict = json.loads(content)
        list = 处理返回字典将其转换为List(dict)

        if len(list) != 0:
            self.将list生成execl文件(stockid, list)
            #for e in list:
                #print(e)



    def 将list生成execl文件(self,stockid,list):
        #生产要保存的文件
        base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        dirname = "%s%s%s%s%s%s" % (
            base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR)
        full_filename = dirname + stockid + pf.Execl

        #转换成dataframe，然后保存成execl
        df =pd.DataFrame(list,columns=['股票代码', '股票名称', '调研次数','调研时间', '公告日期', '接待方式'])
        df.to_excel(full_filename)

        print('上市公司调研情况数据文件已经保存为：\n%s' % (full_filename))



if __name__ == '__main__':
    a = 获取上市公司调研情况_根据股票代码一个一个获取()
    a.根据全量股票进行获取()
