from 数据采集.财务分析.公司利润表 import 获取_全量股票_公司利润表_某个季度
from 数据采集.财务分析.现金流量表 import 获取_全量股票_现金流量表_某个季度
from 数据采集.财务分析.财务指标 import 获取_全量股票_财务指标_某个季度
from 数据采集.财务分析.资产负债表 import 获取_全量股票_资产负债表_某个季度

from 数据采集.财务分析.财务分析_对外接口 import 财务分析_整理某个季度所有基本面数据

def 获取财务分析数据(year,quarter):
    获取_全量股票_公司利润表_某个季度(year,quarter)
    获取_全量股票_现金流量表_某个季度(year,quarter)
    获取_全量股票_财务指标_某个季度(year,quarter)
    获取_全量股票_资产负债表_某个季度(year,quarter)

def 整理获取的财务分析数据(year,quarter):
    财务分析_整理某个季度所有基本面数据(year,quarter)

def 数据采集加整理一个季度的数据(year,quarter):
    获取财务分析数据(year, quarter)
    整理获取的财务分析数据(str(year), str(quarter))

if __name__ == '__main__':
    数据采集加整理一个季度的数据(2019, 4)
