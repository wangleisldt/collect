from 数据采集.财务分析.公司利润表 import 获取_全量股票_公司利润表_某个季度
from 数据采集.财务分析.现金流量表 import 获取_全量股票_现金流量表_某个季度
from 数据采集.财务分析.财务指标 import 获取_全量股票_财务指标_某个季度
from 数据采集.财务分析.资产负债表 import 获取_全量股票_资产负债表_某个季度



def 获取财务分析数据(year,quarter):

    获取_全量股票_公司利润表_某个季度(year,quarter)
    获取_全量股票_现金流量表_某个季度(year,quarter)
    获取_全量股票_财务指标_某个季度(year,quarter)
    获取_全量股票_资产负债表_某个季度(year,quarter)

def 获取财务分析数据_年(year):

    获取财务分析数据(year, 1)
    获取财务分析数据(year, 2)
    获取财务分析数据(year, 3)
    获取财务分析数据(year, 4)

if __name__ == '__main__':
    获取财务分析数据(2019, 2)
    #获取财务分析数据(2011, 2)
    #获取财务分析数据(2011, 3)
    #获取财务分析数据(2006, 4)


    #获取财务分析数据_年(1999)

