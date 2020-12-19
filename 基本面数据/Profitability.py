import tushare as ts

from 函数目录 import profile as pf, date

from 函数目录.function import checkAndCreateDir

class ProfitAbility:
    # 初始化
    def __init__(self):
        #文件存放的目录
        self.ProfitAbility = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.ProfitAbility + pf.SEPARATOR
        #年
        self.YEAR = ""
        #季度
        self.QUARTER = ""

#################################################
# 根据季度，获取股票基本面数据
# 入参1，年份 2015
# 入参2，季度 1
#################################################
    def getProfitAbility(self):
        try:
            checkAndCreateDir(self.ProfitAbility)
            data = ts.get_profit_data(self.YEAR, self.QUARTER)
            filename = '%s%i%i%s' % (self.ProfitAbility,self.YEAR,self.QUARTER,".xlsx")
            data.to_excel(filename)
            #可以增加csv文件保存
            #filename = '%s%i%i%s' % (self.ProfitAbility, self.YEAR, self.QUARTER, ".csv")
            #data.to_csv(filename)
        except:
            print("获取当年失败！")

#################################################
# 根据季度，获取股票基本面数据（当年）
#################################################
    def getProfitAbilityThisYear(self):
        try:
            for element in date.getCurrentQuarterList():
                self.YEAR = date.getCurrentYear()
                self.QUARTER = element
                self.getProfitAbility()
        except:
            pass

#################################################
# 获取股票某年基本面数据
# 入参1，年份 如 2015
#################################################
    def getProfitAbilityYear(self,year):
        print("%s%s%s" % ("\n开始获取", year, "年的盈利能力："))
        if year != date.getCurrentYear():
            for i in range(1, 4+1):
                self.YEAR = year
                self.QUARTER = i
                self.getProfitAbility()
        else:
            self.getProfitAbilityThisYear()

#################################################
# 获取股票某几年基本面数据
# 入参1，前年份 如 2015
# 入参1，后年份 如 2017
#################################################
    def getProfitAbilityYearRange(self, yearFront,yearBack):
        for i in range(yearFront, yearBack+1):
            self.getProfitAbilityYear(i)

if __name__ == '__main__':
    aa = ProfitAbility()
    aa.getProfitAbilityYearRange(2017,2017)
