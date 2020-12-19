
import requests
import docx
import os
import jieba
import jieba.analyse
import time
from win32com import client as wc

from 函数目录 import profile as pf
import re
from 函数目录.function import checkAndCreateDir,check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getYearMonthFromMonthLength

def 根据URL返回季度(adjunctUrl,start_quarter):
    list = re.split('/', adjunctUrl)
    year = list[1][0:4]
    month= list[1][5:7]
    quarter = int((int(month)+2)/3)
    url_quarter = "%s%s" % (year,quarter)
    if start_quarter == url_quarter:
        return True , url_quarter
    else:
        return False , url_quarter

def 根据URL和证券代码和采集季度返回保存的文件全路径及是否要保存(adjunctUrl,stockid,start_quarter):
    是否要保存,URL季度 = 根据URL返回季度(adjunctUrl, start_quarter)
    if 是否要保存:
        list = re.split('/', adjunctUrl)
        year = list[1][0:4]
        raw_filename = list[2]
        #生成保存目录名称
        base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        dir_name = "%s%s%s%s%s%s%s%s" % (base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据,pf.SEPARATOR, year, pf.SEPARATOR)
        checkAndCreateDir(dir_name)
        #生成文件名称  例如  002415_20181_2018-03-19_1204492413.PDF
        filename = "%s_%s_%s_%s" % (stockid,URL季度,list[1],raw_filename)
        return dir_name,filename,True
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


def get_announcement_from_juchao(stockid,quarter):
    """
    获取巨潮资讯网站上投资者活动关系
    :param stockid: string e.g. 000860
    :param pause:
    :return:
    """
    url = "http://www.cninfo.com.cn/cninfo-new/announcement/query"
    data = {'stock':stockid,
            'searchkey':'',
            'plate':'',
            'category':'',
            'trade':'',
            'column':'szse',
            'columnTitle':u'历史公告查询',
            'pageNum':1,
            'pageSize':30,
            'tabName':'relation',
            'sortName':'',
            'sortType':'',
            'limit':'',
            'showTitle':u'',
            'seDate':u'请选择日期'}
    response = requests.post(url, data)
    totalAnnouncement = response.json()['totalAnnouncement']
    content = response.json()['announcements']
    for element in content:
        title = element['announcementTitle']
        adjunctUrl = element['adjunctUrl']
        adjunctType = element['adjunctType']
        print(u'股票代码:%s,主题:%s,URL:%s,文件类型:%s' % (stockid,title, adjunctUrl, adjunctType))
        file_url = "http://www.cninfo.com.cn/" + adjunctUrl
        r = requests.get(file_url)
        目录名,文件名称,是否要保存 = 根据URL和证券代码和采集季度返回保存的文件全路径及是否要保存(adjunctUrl, stockid, quarter)
        if 是否要保存:
            #判断文件是否存在
            if check_file_exist(目录名, 文件名称):
                pass
            else:
                with open(os.path.join(目录名, 文件名称), 'wb') as file:
                    file.write(r.content)

def 获取上市公司调研情况接口(startDate,monthLength):
    def 产生需要处理的yearMonthList(startDate,monthLength):
        yearMonthList = []
        for i in range( 0 ,int(monthLength)):
            yearMonth = getYearMonthFromMonthLength(startDate, i)
            yearMonthList.append(yearMonth)
        yearMonthList.sort()
        return yearMonthList

    yearMonthList = 产生需要处理的yearMonthList(startDate, monthLength)




if __name__ == '__main__':

    stockListInstance = StockDict()
    for element in stockListInstance.stockIdList:
        generator = get_announcement_from_juchao(element,"20181")

