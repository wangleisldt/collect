import pickle

import tushare as ts

from 函数目录 import profile as pf, date

from 函数目录.function import checkAndCreateDir

def getStockList():
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
        #filename = '%s%s%s%s' % (StockListDir, pf.StockListFilename, date.getCurrentDate(), pf.Execl)
        filenameDate = '%s%s%s' % (StockListDir, pf.StockListFilename, pf.Execl)
        #data.to_excel(filename)
        data.to_excel(filenameDate)

        # 保存成pkl文件
        #filename = '%s%s%s%s' % (StockListDir, pf.StockListFilename, date.getCurrentDate(), pf.PklFile)
        filenameDate = '%s%s%s' % (StockListDir, pf.StockListFilename, pf.PklFile)
        #output = open(filename, 'wb')
        #pickle.dump(stockDict, output)
        #output.close()
        output = open(filenameDate, 'wb')
        pickle.dump(stockDict, output)
        output.close()

        print("结束获取股票列表")

    except:
        print("获取失败")

if __name__ == '__main__':
    getStockList()