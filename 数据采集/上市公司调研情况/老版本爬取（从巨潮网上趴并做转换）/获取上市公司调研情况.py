import requests
import os


from 函数目录 import profile as pf
import re
from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getYearMonthFromMonthLength

import time

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
        count = 0
        for stockId in stockListInstance.stockIdList:
            if count == 300 :
                time.sleep(5)
                print('网页查询了300个股票等待5秒！')
                count = 0
            else:
                count = count +1
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
    获取上市公司调研情况(yearMonth, monthLength)

if __name__ == '__main__':

    获取上市公司调研情况接口('201805',4)
