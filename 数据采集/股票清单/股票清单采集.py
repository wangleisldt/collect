import pickle
from 函数目录 import profile as pf, date
from 函数目录.function import checkAndCreateDir
import pandas as pd
from 数据采集.标准类.采集标准类 import 采集标准类
import joblib

'''

def getStockList_old():
    try:
        print("开始获取股票列表")
        StockListDir = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.StockList + pf.SEPARATOR
        #获取数据
        data = ts.get_stock_basics()
        #转换为字典
        stockDict = data.to_dict()
        data = data.sort_index(axis=0)#对数据进行排序
        #print(data)


        checkAndCreateDir(StockListDir)

        # 保存成execl文件
        filename = '%s%s%s%s' % (StockListDir, pf.StockListFilename, date.getCurrentDate(), pf.Execl)
        filenameDate = '%s%s%s' % (StockListDir, pf.StockListFilename, pf.Execl)
        data.to_excel(filename)
        data.to_excel(filenameDate)

        # 保存成pkl文件
        filename = '%s%s%s%s' % (StockListDir, pf.StockListFilename, date.getCurrentDate(), pf.PklFile)
        filenameDate = '%s%s%s' % (StockListDir, pf.StockListFilename, pf.PklFile)
        output = open(filename, 'wb')
        pickle.dump(stockDict, output)
        output.close()
        output = open(filenameDate, 'wb')
        pickle.dump(stockDict, output)
        output.close()

        print("结束获取股票列表")

    except:
        print("获取失败")
'''


def _处理返回值(content):
    stock_list = content["data"]["diff"]

    df = pd.DataFrame(stock_list)
    return_df = df[['f12','f14','f15','f3','f4','f5','f6','f7','f15','f16','f17','f18','f10','f8','f9','f23','f20','f21','f24','f25','f26','f27']]
    return_df.columns = pf.股票清单表头

    return return_df

def _根据参数产生url(page_size=90000000):
    url = "http://91.push2.eastmoney.com/api/qt/clist/get?pn=1&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23".format(page_size)
    return url

def getStockList():
    try:
        print("开始获取股票列表")
        StockListDir = pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.StockList + pf.SEPARATOR
        #获取数据
        instance = 采集标准类(url=_根据参数产生url())
        content = instance._获取数据_json()
        data = _处理返回值(content)

        data = data.sort_values(axis=0,by=pf.股票清单表头[0])#对数据进行排序
        #data = data.reset_index(drop=True)

        # 转换为字典
        stockDict = data.set_index(pf.股票清单表头[0]).to_dict()

        print("结束获取股票列表")
        print("开始保存股票列表")

        checkAndCreateDir(StockListDir)

        # 保存成execl文件
        filename = '%s%s%s%s' % (StockListDir, pf.StockListFilename, date.getCurrentDate(), pf.Execl)
        filenameDate = '%s%s%s' % (StockListDir, pf.StockListFilename, pf.Execl)
        data.to_excel(filename,index=False)
        data.to_excel(filenameDate,index=False)

        # 保存成pkl文件
        filename = '%s%s%s%s' % (StockListDir, pf.StockListFilename, date.getCurrentDate(), pf.PklFile)
        filenameDate = '%s%s%s' % (StockListDir, pf.StockListFilename, pf.PklFile)
        output = open(filename, 'wb')
        pickle.dump(stockDict, output)
        output.close()
        output = open(filenameDate, 'wb')
        pickle.dump(stockDict, output)
        output.close()

        filename = '%s%s%s' % (StockListDir, pf.StockListFilename, pf.GZ)
        joblib.dump(stockDict, filename, compress=3 , protocol=None)
        filename = '%s%s%s%s' % (StockListDir, pf.StockListFilename, date.getCurrentDate(), pf.GZ)
        joblib.dump(stockDict, filename, compress=3, protocol=None)

        print("结束保存股票列表")

    except:
        print("获取失败")

if __name__ == '__main__':
    getStockList()

'''
filename = '/home/wangleisldt/collect_data/基本面数据/股票列表/stocklist.gz'
    obj = joblib.load(filename, mmap_mode=None)

    print(type(obj))

    for k,v in obj.items():
        print(k,'-------',v)

'''

