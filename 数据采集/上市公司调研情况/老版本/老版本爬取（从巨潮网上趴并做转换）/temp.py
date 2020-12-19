import requests
import docx
import os
import jieba
import jieba.analyse
import time
from win32com import client as wc

from 函数目录 import profile as pf
import re
from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getYearMonthFromMonthLength


def 根据URL返回季度(adjunctUrl, start_quarter):
    list = re.split('/', adjunctUrl)
    year = list[1][0:4]
    month = list[1][5:7]
    quarter = int((int(month) + 2) / 3)
    url_quarter = "%s%s" % (year, quarter)
    if start_quarter == url_quarter:
        return True, url_quarter
    else:
        return False, url_quarter


def 根据URL和证券代码和采集季度返回保存的文件全路径及是否要保存(adjunctUrl, stockid, start_quarter):
    是否要保存, URL季度 = 根据URL返回季度(adjunctUrl, start_quarter)
    if 是否要保存:
        list = re.split('/', adjunctUrl)
        year = list[1][0:4]
        raw_filename = list[2]
        # 生成保存目录名称
        base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        dir_name = "%s%s%s%s%s%s%s%s" % (
        base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR, year, pf.SEPARATOR)
        checkAndCreateDir(dir_name)
        # 生成文件名称  例如  002415_20181_2018-03-19_1204492413.PDF
        filename = "%s_%s_%s_%s" % (stockid, URL季度, list[1], raw_filename)
        return dir_name, filename, True
    else:
        '''list = re.split('/', adjunctUrl)
        year = list[1][0:4]
        raw_filename = list[2]
        # 生成保存目录名称
        base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        dir_name = "%s%s%s%s%s%s%s%s" % (
        base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR, year, pf.SEPARATOR)
        checkAndCreateDir(dir_name)
        # 生成文件名称  例如  002415_20181_2018-03-19_1204492413.PDF
        filename = "%s_%s_%s_%s" % (stockid, URL季度, list[1], raw_filename)
        return dir_name, filename, True'''
        return None, None, False


def get_announcement_from_juchao(stockid, quarter):
    """
    获取巨潮资讯网站上投资者活动关系
    :param stockid: string e.g. 000860
    :param pause:
    :return:
    """
    url = "http://www.cninfo.com.cn/cninfo-new/announcement/query"
    data = {'stock': stockid,
            'searchkey': '',
            'plate': '',
            'category': '',
            'trade': '',
            'column': 'szse',
            'columnTitle': u'历史公告查询',
            'pageNum': 1,
            'pageSize': 30,
            'tabName': 'relation',
            'sortName': '',
            'sortType': '',
            'limit': '',
            'showTitle': u'',
            'seDate': u'请选择日期'}
    response = requests.post(url, data)
    totalAnnouncement = response.json()['totalAnnouncement']
    content = response.json()['announcements']
    for element in content:
        title = element['announcementTitle']
        adjunctUrl = element['adjunctUrl']
        adjunctType = element['adjunctType']
        print(u'股票代码:%s,主题:%s,URL:%s,文件类型:%s' % (stockid, title, adjunctUrl, adjunctType))
        file_url = "http://www.cninfo.com.cn/" + adjunctUrl
        r = requests.get(file_url)
        目录名, 文件名称, 是否要保存 = 根据URL和证券代码和采集季度返回保存的文件全路径及是否要保存(adjunctUrl, stockid, quarter)
        if 是否要保存:
            # 判断文件是否存在
            if check_file_exist(目录名, 文件名称):
                pass
            else:
                with open(os.path.join(目录名, 文件名称), 'wb') as file:
                    file.write(r.content)

class 获取上市公司调研情况():
    # 初始化
    def __init__(self, startDate, monthLength):
        self.startDate = startDate  # 201808
        self.monthLength = monthLength  # 几个月（步长）

        self.yearMonthList = [] #存放类似 ['201804','201805','201806','201807']

        self.产生需要处理的yearMonthList()
        self.获取上市公司调研情况文件()

    def 产生需要处理的yearMonthList(self):
        for i in range( 0 ,int(self.monthLength)):
            yearMonth = getYearMonthFromMonthLength(self.startDate, i)
            self.yearMonthList.append(yearMonth)
        self.yearMonthList.sort()

    def 获取上市公司调研情况文件(self):
        stockListInstance = StockDict()
        for stockId in stockListInstance.stockIdList:
            self.获取单个上市公司调研情况文件(stockId)

    def 获取单个上市公司调研情况文件(self,stockid):
        """
            获取巨潮资讯网站上投资者活动关系
            :param stockid: string e.g. 000860
            :param pause:
            :return:
            """
        url = "http://www.cninfo.com.cn/cninfo-new/announcement/query"
        data = {'stock': stockid,
                'searchkey': '',
                'plate': '',
                'category': '',
                'trade': '',
                'column': 'szse',
                'columnTitle': u'历史公告查询',
                'pageNum': 1,
                'pageSize': 30,
                'tabName': 'relation',
                'sortName': '',
                'sortType': '',
                'limit': '',
                'showTitle': u'',
                'seDate': u'请选择日期'}
        response = requests.post(url, data)
        totalAnnouncement = response.json()['totalAnnouncement']
        content = response.json()['announcements']
        for element in content:
            title = element['announcementTitle']
            adjunctUrl = element['adjunctUrl']
            adjunctType = element['adjunctType']
            #print(u'股票代码:%s,主题:%s,URL:%s,文件类型:%s' % (stockid, title, adjunctUrl, adjunctType))
            file_url = "http://www.cninfo.com.cn/" + adjunctUrl
            returnList = self.根据URL和证券代码和文件类型返回保存的文件全路径及是否要保存(adjunctUrl, adjunctType, stockid)
            if returnList[0]:
                print(u'股票代码:%s,主题:%s,URL:%s,文件类型:%s' % (stockid, title, adjunctUrl, adjunctType))
                r = requests.get(file_url)
                with open(os.path.join(returnList[1]), 'wb') as file:
                    file.write(r.content)
            else:
                pass


    def 根据URL和证券代码和文件类型返回保存的文件全路径及是否要保存(self,adjunctUrl, adjunctType,stockid ):
        def 时间是否在需要保存的范围内(yearMonth):
            if yearMonth in self.yearMonthList:
                return True
            else:
                return False


        def 文件是否在原有目录里面不存在(文件名前缀,stockid,date,adjunctType):
            def 生成需要保存的文件名前缀(文件名前缀,stockid,date):
                quarter = int((int(date[5:7]) + 2) / 3)
                file_quarter = "%s%s" % (date[0:4], quarter)
                return '%s_%s_%s_%s' % (stockid,file_quarter,date,文件名前缀)

            def 检测文件是否存在(文件名前缀, date, 后缀):
                year = date[0:4]
                # 生成保存目录名称
                base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
                dir_name = "%s%s%s%s%s%s%s" % (
                    base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR, year)
                #checkAndCreateDir(dir_name)
                filename = '%s.%s' % (文件名前缀, 后缀)
                #print(dir_name,filename)
                return check_file_exist(dir_name, filename)


            生成的文件名前缀 = 生成需要保存的文件名前缀(文件名前缀, stockid, date)
            if adjunctType in ['PDF', 'DOCX' ] :
                if 检测文件是否存在(生成的文件名前缀,date,adjunctType) is False:
                    return True, 生成的文件名前缀
                else:
                    return False, ''
            elif adjunctType == 'DOC':
                if 检测文件是否存在(生成的文件名前缀,date,'DOCX') is True:
                    return False, ''
                elif 检测文件是否存在(生成的文件名前缀, date, 'DOC') is True:
                    return False, ''
                else:
                    return True, 生成的文件名前缀
            else:
                return False,''


        yearMonth, 文件名前缀, 文件名后缀,date = self.根据URL返回日期和文件名前缀和后缀(adjunctUrl)
        #print(文件名前缀,文件名后缀)

        #根据几个条件判断文件是否要保存
        #1、时间是否在需要保存的范围内
        #2、文件是否在原有目录里面存在
        if 时间是否在需要保存的范围内(yearMonth):
            returnList = 文件是否在原有目录里面不存在(文件名前缀,stockid,date,adjunctType)
            if returnList[0]:
                year = date[0:4]
                base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
                dir_name = "%s%s%s%s%s%s%s%s" % (
                    base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR, year, pf.SEPARATOR)
                fullfilename = '%s%s.%s' % (dir_name,returnList[1],文件名后缀)
                return True,fullfilename
            else:
                return False,''
        else:
            return False,''



    def 根据URL返回日期和文件名前缀和后缀(self,adjunctUrl):#返回  201808 , 1205033095 , DOCX
        list = re.split('/', adjunctUrl)
        year = list[1][0:4]
        month = list[1][5:7]
        yearMonth = '%s%s' % (year,month)
        date = list[1][0:10]
        raw_filename = list[2]
        #print(raw_filename)
        list1 = raw_filename.split('.')
        文件名前缀 = list1[0]
        文件名后缀 = list1[1]
        return yearMonth,文件名前缀,文件名后缀,date

def 获取上市公司调研情况接口(yearMonth,monthLength):
    获取上市公司调研情况('201805', 4)

if __name__ == '__main__':

    获取上市公司调研情况接口('201805',4)
