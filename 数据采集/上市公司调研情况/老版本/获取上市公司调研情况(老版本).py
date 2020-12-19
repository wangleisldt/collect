import requests
import json
import pickle

import os

from 函数目录 import profile as pf
import re
from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getYearMonthFromMonthLength

import time

class 获取上市公司调研情况():
    # 初始化
    def __init__(self,date):
        self.是否要继续获取数据 = True
        self.date = date

    def 获取多页数据(self):
        pageNum = 1
        while self.是否要继续获取数据:
            self.获取数据(pageNum)
            pageNum = pageNum + 1

    def 获取数据(self,pageNum):
        """
            获取东方财富网投资者活动关系
            :param stockid: string e.g. 000860
            :param pause:
            :return:
            """
        #url = "http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=50&page=%s&js=var%%20CSsawKhe&param=&sortRule=-1&sortType=0&rt=51223964" % (pageNum)
        url = "http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=50&page=%s&js=var%%20CSsawKhe&param=&sortRule=-1&sortType=0" % (
            pageNum)

        print("开始获取第%s页数据。" %  (pageNum))
        response = requests.post(url)
        #print(response.content.decode('GBK'))
        content = response.content.decode('GBK')[13:]

        dict = json.loads(content)
        #print(dict['pages'])
        #print(dict['data'])

        list = self.处理返回字典将其转换为List(dict)

        for e in list:
            print(e)

        self.将数据保存到每个股票文件中(list)

    def 处理返回字典将其转换为List(self,dict):
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
        return returnList

    def 将数据保存到每个股票文件中(self,list):
        def 检测文件是否存在(文件名前缀, 后缀):
            # 生成保存目录名称
            base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
            dirname = "%s%s%s%s%s%s" % (
                base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR)
            checkAndCreateDir(dirname)
            filename = '%s%s' % (文件名前缀, 后缀)
            # print(dir_name,filename)
            return check_file_exist(dirname, filename)

        def 将字典保存成文件(dict, stockId):
            # 产生需要打开的目录
            base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
            dirname = "%s%s%s%s%s%s" % (
                base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR)
            filename = '%s%s%s' % (dirname, stockId, pf.PklFile)
            output = open(filename, 'wb')
            pickle.dump(dict, output)
            output.close()

        def 从文件中读取字典(stockId):
            base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
            dirname = "%s%s%s%s%s%s" % (
                base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR)
            filename = '%s%s%s' % (dirname, stockId, pf.PklFile)
            pklFile = open(filename, 'rb')
            dict = pickle.load(pklFile)
            pklFile.close()

            return dict

        date = "%s-%s-%s" % (self.date[0:4], self.date[4:6], self.date[6:8])

        for element in list:
            if element[4] >= date:
                #print(element[4],date)
                #print(element)
                if 检测文件是否存在(element[0],pf.PklFile):
                    dict = 从文件中读取字典(element[0])
                    #for key, value in dict.items():
                    #   print(key, ' value : ', value)
                    if element[3] not in dict.keys():
                        print("旧保存数据 %s" % (element))
                        dict[element[3]] = element
                        将字典保存成文件(dict, element[0])
                else:
                    dict={}
                    #不存在，产生要保存的字典
                    print("新保存数据 %s" % (element))
                    dict[element[3]]= element
                    #保存dict到pkl文件中
                    将字典保存成文件(dict, element[0])
            else:
                self.是否要继续获取数据 = False

if __name__ == '__main__':
    a = 获取上市公司调研情况("20180701")
    a.获取多页数据()
