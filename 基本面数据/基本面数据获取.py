import 基本面数据.PerformanceReport as pr
import 基本面数据.OperationCapacity as oc
import 基本面数据.GrowthAbility as ga
import 基本面数据.DebtPayingAbility as dpa
import 基本面数据.CashFlow as cf
import 基本面数据.Profitability as pf


#################################################
# 获取某些年份的基本面数据
# 入参1，起始年份 2015  数字
# 入参2，终止年份 2017  数字
#################################################
def 基本面数据获取(fromYear,toYear):

    aa = pr.PerformanceReport()
    aa.getPerformanceReportYearRange(fromYear, toYear)
    aa = oc.OperationCapacity()
    aa.getOperationCapacityYearRange(fromYear, toYear)
    aa = ga.GrowthAbility()
    aa.getGrowthAbilityYearRange(fromYear, toYear)
    aa = dpa.DebtPayingAbility()
    aa.getDebtPayingAbilityYearRange(fromYear, toYear)
    aa = cf.CashFlow()
    aa.getCashFlowYearRange(fromYear, toYear)
    aa = pf.ProfitAbility()
    aa.getProfitAbilityYearRange(fromYear, toYear)

#################################################
# 获取某个季度的基本面数据
# 入参1，年份 2015  数字
# 入参2，季度 1  数字
#################################################
def 季度基本面数据获取(year,quarter):

    print("%s%s%s%s" % ("\n开始获取", year, quarter , "年的业绩报告（主表）："))
    aa = pr.PerformanceReport()
    aa.YEAR = year
    aa.QUARTER = quarter
    aa.getPerformanceReport()

    print("%s%s%s%s" % ("\n开始获取", year, quarter, "年的营运能力："))
    aa = oc.OperationCapacity()
    aa.YEAR = year
    aa.QUARTER = quarter
    aa.getOperationCapacity()

    print("%s%s%s%s" % ("\n开始获取", year, quarter, "年的成长能力："))
    aa = ga.GrowthAbility()
    aa.YEAR = year
    aa.QUARTER = quarter
    aa.getGrowthAbility()

    print("%s%s%s%s" % ("\n开始获取", year, quarter, "年的偿债能力："))
    aa = dpa.DebtPayingAbility()
    aa.YEAR = year
    aa.QUARTER = quarter
    aa.getDebtPayingAbility()

    print("%s%s%s%s" % ("\n开始获取", year, quarter, "年的现金流量："))
    aa = cf.CashFlow()
    aa.YEAR = year
    aa.QUARTER = quarter
    aa.getCashFlow()

    print("%s%s%s%s" % ("\n开始获取", year, quarter, "年的盈利能力："))
    aa = pf.ProfitAbility()
    aa.YEAR = year
    aa.QUARTER = quarter
    aa.getProfitAbility()

if __name__ == '__main__':
    fromYear = 2015
    toYear = 2019

    aa = pr.PerformanceReport()
    aa.getPerformanceReportYearRange(fromYear, toYear)
    aa = oc.OperationCapacity()
    aa.getOperationCapacityYearRange(fromYear, toYear)
    aa = ga.GrowthAbility()
    aa.getGrowthAbilityYearRange(fromYear, toYear)
    aa = dpa.DebtPayingAbility()
    aa.getDebtPayingAbilityYearRange(fromYear, toYear)
    aa = cf.CashFlow()
    aa.getCashFlowYearRange(fromYear, toYear)
    aa = pf.ProfitAbility()
    aa.getProfitAbilityYearRange(fromYear, toYear)
