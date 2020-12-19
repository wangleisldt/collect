import pickle

import tushare as ts

from 函数目录 import profile as pf, function


def getRealtimeQuotesDataToExecl():
    try:
        # 获取实时行情
        print("开始获取股票实时行情数据")
        dir = pf.GLOBAL_PATH + pf.SEPARATOR + pf.TransactionData + pf.SEPARATOR + pf.RealtimeQuotesData + pf.SEPARATOR
        filename = dir + pf.StockRealtimeQuotesDataFilename + pf.Execl
        function.checkAndCreateDir(dir)
        df = ts.get_today_all()
        df.to_excel(filename)

        dict = df.to_dict()
        filename = dir + pf.StockRealtimeQuotesDataFilename + pf.PklFile
        outputFile = open(filename, 'wb')
        pickle.dump(dict, outputFile)
        print("\n获取实时行情成功")
    except:
        print("\n获取实时行情失败")

class realtimeStockPrice:
    # 初始化
    def __init__(self, StockId=""):

        # pkl文件名称
        dir = pf.GLOBAL_PATH + pf.SEPARATOR + pf.TransactionData + pf.SEPARATOR + pf.RealtimeQuotesData + pf.SEPARATOR
        self.filename = dir + pf.StockRealtimeQuotesDataFilename + pf.PklFile
        self.stockDict = function.getPklDataToDict(self.filename)

    def getRealtimeStockPrice(self,stockId):
        for key, value in self.stockDict["code"].items():
            if value == stockId:
                return self.stockDict["trade"][key]
        return None

if __name__ == '__main__':
    #getRealtimeQuotesDataToExecl()

    aa = realtimeStockPrice()
    price = aa.getRealtimeStockPrice("600663")
    print(price)

