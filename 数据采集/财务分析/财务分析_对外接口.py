from 数据采集.财务分析.相关数据采集 import 获取财务分析数据
from 数据采集.财务分析.财务分析_数据整理 import 处理某个季度

def 财务分析_获取某个季度的数据(year,quarter):
    获取财务分析数据(year, quarter)

def 财务分析_整理某个季度所有基本面数据(year,quarter):
    处理某个季度(str(year),str(quarter))

def 数据采集加整理一个季度的数据(year,quarter):
    财务分析_获取某个季度的数据(year, quarter)
    财务分析_整理某个季度所有基本面数据(str(year), str(quarter))