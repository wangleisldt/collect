# encoding:utf-8

import 数据采集.股票清单.股票清单采集 as gplist

import 交易数据.实时交易数据 as rt

import 基本面数据.基本面数据获取 as jbmget

if __name__ == '__main__':
    #获取股票清单
    gplist.getStockList()

    #获取股票实时行情
    #rt.getRealtimeQuotesDataToExecl()

    #基本面数据获取
    #根据年度来
    #jbmget.基本面数据获取(2017,2017)
    #根据季度来(2017年4季度)
    jbmget.季度基本面数据获取(2020, 3)
