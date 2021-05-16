# encoding:utf-8
#
# import pandas as pd
from 函数目录 import profile as pf
from 函数目录.date import get_1_quarter_after
from 数据采集.股票清单.股票清单获取 import StockDict
from 数据采集.标准类.采集标准类 import 采集标准类
from 数据采集.三张报表.采集企业类型 import 读取企业类型
from 数据采集.三张报表.财务指标读取 import 财务指标读取
import json
from 函数目录.function import checkAndCreateDir
import joblib
import time

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

财务指标报表类型 = {
        '主要指标': 'MainTarget',
        '资产负债表' : 'zcfzb',
        '现金流量表': 'xjllb',
        '利润表': 'lrb',
    }

def 根据全量股票进行获取(year, quarter,report_type_in):
    end_date = _将年季度转换为后一个季度末日期(year, quarter)
    report_type = 财务指标报表类型[report_type_in]
    stockid_market_list = _获取股票清单和交易市场()

    try:
        之前采集的财务指标_dict = 财务指标读取(report_type_in,f'{year}{quarter}')
    except:
        之前采集的财务指标_dict = {}

    #print(stockid_market_list)
    print("开始获取数据：")
    return_dict = {}
    for element in stockid_market_list:
        #time.sleep(1)
        stockid, market = element
        print("开始获取%s股票数据" % (stockid))

        # 判断是否之前已经采集过
        if stockid in 之前采集的财务指标_dict.keys():
            return_dict[stockid] = 之前采集的财务指标_dict[stockid]
            print(f'之前已经采集过。')
            continue

        # 之前未采集过，进行采集
        company_type = 读取企业类型()
        if stockid in company_type.keys():
            instance = 采集标准类(url = _根据参数产生url(stockid,market,report_type,end_date = end_date , company_type_dict = company_type ))
            return_list = instance._获取数据_json()
            if report_type != 'MainTarget':
                if return_list is not None:
                    list = json.loads(return_list)
                else:
                    list = None
            else:
                list = return_list

            # print(list)

            if list is not None:
                dict = _处理返回值(list,str(year)+pf.End_OF_SEASON_DAY[quarter],report_type)
                if dict is not None:
                    #print(dict)
                    for k,v in dict.items():
                        # print(k,"------------",v)

                        if len(v) >= 1:
                            try:
                                if v[-1] == '万':
                                    dict[k] = round(float(v[:-1])*10000)
                                elif v[-1] == '亿':
                                    dict[k] = round(float(v[:-1])*100000000)
                                    # print(dict[k])
                            except:
                                pass
                    return_dict[stockid]=dict

                    # print("#######################################")
                    # for k,v in return_dict[stockid].items():
                    #     print(k,v)

                else:
                    print("无数据###")
            else:
                print("无数据。")


    _保存财务分析(return_dict, report_type_in, str(year)+str(quarter))

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
    #print(url)
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

def _保存财务分析(input_dict,type,date):
    base_dir_name = "%s%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA, pf.SEPARATOR)
    dir = base_dir_name + pf.财务分析 + pf.SEPARATOR
    checkAndCreateDir(dir)
    filename_gz = "%s%s%s%s" % (dir, type,date, pf.GZ)

    joblib.dump(input_dict, filename_gz, compress=3, protocol=None)

def 获取全部数据(year,quarter):
    根据全量股票进行获取(year, quarter, '主要指标')
    根据全量股票进行获取(year,quarter, '资产负债表')
    根据全量股票进行获取(year,quarter, '现金流量表')
    根据全量股票进行获取(year,quarter, '利润表')


if __name__ == '__main__':

    #获取全部季度数据(2018,1)

    # 根据全量股票进行获取(2020,1 , '主要指标')
    # 根据全量股票进行获取( 2020,4 , '资产负债表')
    根据全量股票进行获取(2015, 2, '现金流量表')
    # 根据全量股票进行获取(2015, 2, '利润表')
