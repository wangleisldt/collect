# encoding:utf-8


from 数据采集.三张报表.采集企业类型 import 采集企业类型
from 数据采集.三张报表.财务指标采集 import 根据全量股票进行获取


def 采集企业类型接口(是否读取原有数据=True):
    采集企业类型(是否读取原有数据)

def 获取全部季度数据(year,quarter):
    根据全量股票进行获取(year, quarter, '主要指标')
    根据全量股票进行获取(year, quarter, '资产负债表')
    根据全量股票进行获取(year, quarter, '现金流量表')
    根据全量股票进行获取(year, quarter, '利润表')

def 获取年度数据(year):
    获取全部季度数据(year, 1)
    获取全部季度数据(year, 2)
    获取全部季度数据(year, 3)
    获取全部季度数据(year, 4)

if __name__ == '__main__':

    采集企业类型接口(是否读取原有数据=True)

    获取全部季度数据(2020, 4)

    获取年度数据(2020)