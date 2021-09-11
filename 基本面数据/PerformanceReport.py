import tushare as ts
from pathlib import Path
from 函数目录 import profile as pf, date


class PerformanceReport:
    # 初始化
    def __init__(self):
        #文件存放的目录
        self.PerformanceReport = Path(pf.GLOBAL_PATH, pf.FUNDAMENTAL_DATA, pf.PerformanceReport)
        self.PerformanceReport.mkdir(exist_ok=True, parents=True)
        # self.PerformanceReport = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.PerformanceReport + pf.SEPARATOR
        #年
        self.YEAR = ""
        #季度
        self.QUARTER = ""

#################################################
# 根据季度，获取股票基本面数据
# 入参1，年份 2015
# 入参2，季度 1
#################################################
    def getPerformanceReport(self):
        try:
            # checkAndCreateDir(self.PerformanceReport)
            data = ts.get_report_data(self.YEAR, self.QUARTER)
            filename = Path(self.PerformanceReport, str(self.YEAR) + str(self.QUARTER) + pf.Execl)
            # filename = '%s%i%i%s' % (self.PerformanceReport,self.YEAR,self.QUARTER,".xlsx")
            data.to_excel(filename)
            #可以增加csv文件保存
            #filename = '%s%i%i%s' % (self.PerformanceReport, self.YEAR, self.QUARTER, ".csv")
            #data.to_csv(filename)
        except:
            print("获取当年失败！")

#################################################
# 根据季度，获取股票基本面数据（当年）
#################################################
    def getPerformanceReportThisYear(self):
        try:
            for element in date.getCurrentQuarterList():
                self.YEAR = date.getCurrentYear()
                self.QUARTER = element
                self.getPerformanceReport()
        except:
            pass

#################################################
# 获取股票某年基本面数据
# 入参1，年份 如 2015
#################################################
    def getPerformanceReportYear(self,year):
        print("%s%s%s" % ("\n开始获取", year, "年的业绩报告（主表）："))
        if year != date.getCurrentYear():
            for i in range(1, 4+1):
                self.YEAR = year
                self.QUARTER = i
                self.getPerformanceReport()
        else:
            self.getPerformanceReportThisYear()

#################################################
# 获取股票某几年基本面数据
# 入参1，前年份 如 2015
# 入参1，后年份 如 2017
#################################################
    def getPerformanceReportYearRange(self, yearFront,yearBack):
        for i in range(yearFront, yearBack+1):
            self.getPerformanceReportYear(i)

if __name__ == '__main__':
    aa = PerformanceReport()
    aa.getPerformanceReportYearRange(2017,2017)
