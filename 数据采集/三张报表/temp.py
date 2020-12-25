import pandas as pd
from 函数目录 import profile as pf
from 函数目录.date import get_1_quarter_after
from 数据采集.股票清单.股票清单获取 import StockDict
from 数据采集.标准类.采集标准类 import 采集标准类
from 数据采集.交易数据.交易数据保存 import 保存交易数据
import json

'''
总表
http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?type=0&code=SZ002507
利润表
http://f10.eastmoney.com/NewFinanceAnalysis/lrbAjax?companyType=4&reportDateType=0&reportType=1&endDate=&code=SZ002507
现金流量表
http://f10.eastmoney.com/NewFinanceAnalysis/xjllbAjax?companyType=4&reportDateType=0&reportType=1&endDate=&code=SZ002507
资产负债表
http://f10.eastmoney.com/NewFinanceAnalysis/zcfzbAjax?companyType=4&reportDateType=0&reportType=1&endDate=&code=SZ002507
http://f10.eastmoney.com/NewFinanceAnalysis/zcfzbAjax?companyType=4&reportDateType=0&reportType=1&endDate=2018-06-30&code=SZ002507
'''

报表 = {
        '资产负债表' : 'zcfzb',
        '现金流量表': 'xjllb',
        '利润表': 'lrb',
    }

def 根据全量股票进行获取(year, quarter,type):
    end_date = _将年季度转换为后一个季度末日期(year, quarter)
    type=报表[type]
    stockid_market_list = _获取股票清单和交易市场()

    # print(stockid_market_list)
    print("开始获取数据：")
    return_dict = {}
    for element in stockid_market_list:
        stockid, market = element
        print("开始获取%s股票数据" % (stockid))
        instance = 采集标准类(url = _根据参数产生url(stockid,market,type,end_date = end_date))
        return_list = instance._获取数据_json()
        list = json.loads(return_list)
        if list is not None:
            dict = _处理返回值(list,str(year)+pf.End_OF_SEASON_DAY[quarter])
            if dict is not None:
                return_dict[stockid]=dict
            else:
                print("无数据")
        else:
            print("无数据")

def _获取股票清单和交易市场():
    stockid_market_list = StockDict().stock_id_market
    return stockid_market_list

def _根据参数产生url(stockid,market,type,end_date):
    if market == 0:
        market = 'SZ'
    else:
        market = 'SH'
    url = 'http://f10.eastmoney.com/NewFinanceAnalysis/{}Ajax?companyType=4&reportDateType=0&reportType=1&endDate={}&code={}{}'.format(type,end_date,market,stockid )
    return url

def _处理返回值(list,date):
    year,month,day = date.split('-')
    date = "{}/{}/{}".format(year,int(month),day)
    #print(date)
    if len(list) >1 :
        return_dict = list[0]
        if return_dict['REPORTDATE'].split(' ')[0] == date:
            return return_dict
        else:
            return None
    else:
        return None

def _将年季度转换为后一个季度末日期(year ,quarter):
    year,quarter = get_1_quarter_after(year,quarter)
    quarter = pf.End_OF_SEASON_DAY[quarter]
    return str(year)+quarter

def 获取全部数据(year,quarter):
    根据全量股票进行获取(year,quarter, '资产负债表')
    根据全量股票进行获取(year,quarter, '现金流量表')
    根据全量股票进行获取(year,quarter, '利润表')

if __name__ == '__main__':
    根据全量股票进行获取( 2020,1 , '资产负债表')
    根据全量股票进行获取(2020, 3, '现金流量表')
    根据全量股票进行获取(2020, 3, '利润表')
