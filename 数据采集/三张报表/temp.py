import pandas as pd
from 函数目录 import profile as pf
from 函数目录.date import get_1_quarter_after
from 数据采集.股票清单.股票清单获取 import StockDict
from 数据采集.标准类.采集标准类 import 采集标准类
from 数据采集.交易数据.交易数据保存 import 保存交易数据
from 数据采集.三张报表.采集企业类型 import 读取企业类型
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
        '主表': 'MainTarget',
        '资产负债表' : 'zcfzb',
        '现金流量表': 'xjllb',
        '利润表': 'lrb',
    }

def 根据全量股票进行获取(year, quarter,type):
    end_date = _将年季度转换为后一个季度末日期(year, quarter)
    type=报表[type]
    stockid_market_list = _获取股票清单和交易市场()

    #print(stockid_market_list)
    print("开始获取数据：")
    return_dict = {}
    for element in stockid_market_list:
        stockid, market = element
        print("开始获取%s股票数据" % (stockid))
        company_type = 读取企业类型()
        instance = 采集标准类(url = _根据参数产生url(stockid,market,type,end_date = end_date , company_type_dict = company_type ))
        return_list = instance._获取数据_json()
        if type != 'MainTarget':
            list = json.loads(return_list)
        else:
            list = return_list
        if list is not None:
            dict = _处理返回值(list,str(year)+pf.End_OF_SEASON_DAY[quarter],type)
            if dict is not None:
                print(dict)
                #for k,v in dict.items():
                    #print(k,"------------",v)
                return_dict[stockid]=dict
            else:
                print("无数据")
        else:
            print("无数据")

def _获取股票清单和交易市场():
    stockid_market_list = StockDict().stock_id_market_sh_sz
    return stockid_market_list

def _根据参数产生url(stockid,market,type,end_date,company_type_dict):
    '''
    按报告期
    reportdatetype="0" reporttype="1"
    按年度
    reportdatetype="1" reporttype="1"
    按单季度
    reportdatetype="0" reporttype="2"
    报告期同比
    reportdatetype="0" reporttype="1"
    年度同比
    reportdatetype="1" reporttype="1"
    单季度环比
    reportdatetype="0" reporttype="2"
    companyType=是直接传过来的，需要再拿一次，有1,2,3,4之区分
    访问这个网页，定位这一行即可
    http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=sz000001
    <input id="hidctype" type="hidden" value="3" />
    '''
    if type == 'MainTarget':
        url = 'http://f10.eastmoney.com/NewFinanceAnalysis/{}Ajax?type=0&endDate={}&code={}{}'.format(type,end_date,market,stockid )
    else:
        url = 'http://f10.eastmoney.com/NewFinanceAnalysis/{}Ajax?companyType={}&reportDateType=0&reportType=1&endDate={}&code={}{}'.format(type,company_type_dict[stockid],end_date,market,stockid )
    return url

def _处理返回值(list,date,type):
    year,month,day = date.split('-')
    date_new = "{}/{}/{}".format(year,int(month),day)
    #print(date)
    if len(list) >1 :
        for element in list:
            if type == 'MainTarget':
                if element['date'] == date:
                    return element
            else:
                if element['REPORTDATE'].split(' ')[0] == date_new:
                    return element
        return None
    else:
        return None

def _将年季度转换为后一个季度末日期(year ,quarter):
    year,quarter = get_1_quarter_after(year,quarter)
    quarter = pf.End_OF_SEASON_DAY[quarter]
    return str(year)+quarter

def 获取全部数据(year,quarter):
    根据全量股票进行获取(year, quarter, '主表')
    根据全量股票进行获取(year,quarter, '资产负债表')
    根据全量股票进行获取(year,quarter, '现金流量表')
    根据全量股票进行获取(year,quarter, '利润表')

if __name__ == '__main__':
    #根据全量股票进行获取(2020,3 , '主表')
    #根据全量股票进行获取( 2020,3 , '资产负债表')
    根据全量股票进行获取(2020, 3, '现金流量表')
    #根据全量股票进行获取(2020, 3, '利润表')
