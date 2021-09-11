import tushare as ts
from pathlib import Path
from 函数目录 import profile as pf, date

class OperationCapacity:
    # 初始化
    def __init__(self):
        #文件存放的目录
        self.OperationCapacity = Path(pf.GLOBAL_PATH, pf.FUNDAMENTAL_DATA, pf.OperationCapacity)
        self.OperationCapacity.mkdir(exist_ok=True, parents=True)
        # self.OperationCapacity = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.OperationCapacity + pf.SEPARATOR
        #年
        self.YEAR = ""
        #季度
        self.QUARTER = ""

#################################################
# 根据季度，获取股票基本面数据
# 入参1，年份 2015
# 入参2，季度 1
#################################################
    def getOperationCapacity(self):
        try:
            # checkAndCreateDir(self.OperationCapacity)
            data = ts.get_operation_data(self.YEAR, self.QUARTER)
            filename = Path(self.OperationCapacity, str(self.YEAR) + str(self.QUARTER) + pf.Execl)
            # filename = '%s%i%i%s' % (self.OperationCapacity,self.YEAR,self.QUARTER,".xlsx")
            data.to_excel(filename)
            #可以增加csv文件保存
            #filename = '%s%i%i%s' % (self.OperationCapacity, self.YEAR, self.QUARTER, ".csv")
            #data.to_csv(filename)
        except:
            print("获取当年失败！")

#################################################
# 根据季度，获取股票基本面数据（当年）
#################################################
    def getOperationCapacityThisYear(self):
        try:
            for element in date.getCurrentQuarterList():
                self.YEAR = date.getCurrentYear()
                self.QUARTER = element
                self.getOperationCapacity()
        except:
            pass

#################################################
# 获取股票某年基本面数据
# 入参1，年份 如 2015
#################################################
    def getOperationCapacityYear(self,year):
        print("%s%s%s" % ("\n开始获取", year, "年的营运能力："))
        if year != date.getCurrentYear():
            for i in range(1, 4+1):
                self.YEAR = year
                self.QUARTER = i
                self.getOperationCapacity()
        else:
            self.getOperationCapacityThisYear()

#################################################
# 获取股票某几年基本面数据
# 入参1，前年份 如 2015
# 入参1，后年份 如 2017
#################################################
    def getOperationCapacityYearRange(self, yearFront,yearBack):
        for i in range(yearFront, yearBack+1):
            self.getOperationCapacityYear(i)

if __name__ == '__main__':
    aa = OperationCapacity()
    aa.getOperationCapacityYearRange(2017,2017)
