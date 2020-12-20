# encoding:utf-8

import pickle
from 函数目录 import profile as pf, date
from 函数目录.function import checkAndCreateDir
import json
import pandas as pd

import requests

import chardet

#http://29.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112400009056043906827682_1608387421151&secid=0.002507&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&beg=0&end=20500101&smplmt=460&lmt=1000000&_=1608387421177
URL = "http://29.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery&secid=1.600663&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&beg=0&end=20500101&smplmt=460&lmt=1000000&_=1608387421177"

def 请求数据(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    fencoding = chardet.detect(response.content)
    content = response.content.decode(fencoding['encoding'], errors='ignore')
    #print(content)
    return content

def 处理返回值(content):

    print(content)


    '''
    #str_dict = content.split("(")[1].split(")")[0]
    str_dict = content[content.find('(')+1:-2]
    stock_list = json.loads(str_dict)["data"]["diff"]

    df = pd.DataFrame(stock_list)
    return_df = df[['f12','f14','f15','f3','f4','f5','f6','f7','f15','f16','f17','f18','f10','f8','f9','f23','f20','f21','f24','f25','f26']]
    return_df.columns = pf.股票清单表头
    :param content: 
    :return: 
    '''


    #return return_df

def 获取交易数据(url=URL):
    #try:
        print("开始获取交易数据：")
        #StockListDir = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.StockList + pf.SEPARATOR
        #获取数据
        content = 请求数据(url)

        处理返回值(content)




        #data = 处理返回值(content)

        print("结束保存股票列表")

    #except:
        #print("获取失败")

if __name__ == '__main__':
    获取交易数据(url=URL)