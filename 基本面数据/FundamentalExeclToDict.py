import xlrd

import 函数目录.date as dt
from 函数目录 import profile as pf


class FundamentalExeclToDict:
    # 初始化
    def __init__(self,DirName,Year, Length ,Quarter="4" ):
        #文件存放的目录
        self.DirName = DirName
        #年
        self.Year = Year
        #季度
        self.Quarter = Quarter
        # 多少年或者季度，步长
        self.Length = Length
        #输出
        self.OutputDict = {}

    #################################################
    # 为对外的访问函数，取固定季度，如20153 20143  20133
    #################################################
    def getRangeDataYearToDict(self):
        for i in range(0, self.Length ):
            year = str(int(self.Year) - i)
            self.getQuarterDataToDict( year ,self.Quarter)

    #################################################
    # 为对外的访问函数，取某个季度前的数据，如20153 20152  20151
    #################################################
    def getRangeDataQuarterToDict(self):
        for i in range(0, self.Length):
            date = dt.getYearQuarterMinusQuarter(self.Year,self.Quarter,i)
            self.getQuarterDataToDict(date[0:4], date[4])

    def getQuarterDataToDict( self , year ,quarter):
        try:
            #打开文件，读取每一行，每一列
            filename = self.DirName + year + quarter + pf.Execl
            print("获取文件信息：",filename)
            workbook = xlrd.open_workbook(filename)
            sheet = workbook.sheet_by_index(0)
            rows = sheet.nrows
            cols = sheet.ncols
            for i in range(rows):
                if i != 0 :

                    list = []
                    dict = {}
                    for j in range(cols):
                        segments = str(sheet.cell_value(i, j))
                        list.append(segments)
                    dict = {year+quarter: list[1:] }#最终将一行拼装成一个dict，并加入年和季度作为key
                    self.findDictAndInsert(list[1],year+quarter ,dict)#查找总的数据dict，是否有相关记录，有则拼接，没有则新建
        except:
            print("获取文件信息失败")

    def findDictAndInsert(self , stockId,date,dict1):
        item = self.OutputDict.get(stockId)
        if item  == None :#是否有该股票的数据
            self.OutputDict[stockId] =  dict1 #没有股票数据，为新建，则将传入的dict加入
        else:#有
            if item.get(date) == None:#判断一下是否有重复数据，如果没有重复数据，则合并
                dictMerged = dict(item,**dict1)#下面两句为合并dict
                self.OutputDict[stockId] = dictMerged
            else:#有重复数据，跳过，不做任何动作（因为发现有重复数据）
                pass


if __name__ == '__main__':
    aa = FundamentalExeclToDict( DirName = "C:\\量化\\基本面数据\\成长能力\\" , Year = "2014" ,  Length = 3 , Quarter = "3"  )
    aa.getRangeDataYearToDict()
    #for key in aa.OutputDict:
        #print(key, 'corresponds to', aa.OutputDict[key])

    #aa = FundamentalExeclToDict(DirName="C:\\量化\\基本面数据\\成长能力\\", Year="2014", Length=2, Quarter="4")
    #aa.getRangeDataQuarterToDict()
    for key in aa.OutputDict:
        print(key, 'corresponds to', aa.OutputDict[key])
