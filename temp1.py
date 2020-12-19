from 基本面数据.股票列表获取 import getStockList

from 数据采集.沪深港通持股.沪深港通持股 import 沪深港通持股

from  数据采集.上市公司调研情况.上市公司调研情况_对外接口 import 上市公司调研情况全量获取加数据整理

from  数据采集.沪深港通持股.沪深港通持股数据入库 import 沪深港通持股数据入库

from 数据采集.财务分析.财务分析_对外接口 import 数据采集加整理一个季度的数据

if __name__ == '__main__':

    #获取股票清单
    getStockList()


    #获取季度财务数据
    #数据采集加整理一个季度的数据(2020, 2)

    #test  