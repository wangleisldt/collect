# import pickle

from 函数目录 import profile as pf
import joblib
from pathlib import Path


class StockDict:
    # 初始化
    def __init__(self):
        #self.filename = '%s%s%s' % (pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.StockList + pf.SEPARATOR, pf.StockListFilename, pf.PklFile)
        # self.filename = '%s%s%s' % (pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.StockList + pf.SEPARATOR,pf.StockListFilename, pf.GZ)
        self.filename = Path(pf.GLOBAL_PATH, pf.FUNDAMENTAL_DATA, pf.StockList,pf.StockListFilename + pf.GZ)

        self.stockDict = {}
        self.stockIdList = []
        self.stock_id_market = []
        self.stock_id_market_sh_sz = []
        self.stockIdListWithoutNone = []
        self.stockIdListWithNone = []

        self.getStockFromFileToDict()
        self.getStockId()
        self.get_stockid_market()
        self.get_stockid_market_sh_sz()
        self.getStockIdWithoutNone()
        self.getStockIdWithNone()

    #################################################
    # 获取股票清单到Dict(类初始化时自动加载)
    #################################################
    def getStockFromFileToDict(self):
        #pklFile = open( self.filename , 'rb')
        #self.stockDict = pickle.load(pklFile)
        #pklFile.close()
        self.stockDict = joblib.load(self.filename, mmap_mode=None)

    #################################################
    # 从股票字典获取股票代码
    #################################################
    def getStockId(self):
        #for stockId in self.stockDict["timeToMarket"]:
        for stockId in self.stockDict[pf.股票清单表头[1]]:
            #print(stockId)
            self.stockIdList.append(str(stockId))
        self.stockIdList.sort()

    #################################################
    # 从股票字典获取股票代码和交易市场
    #################################################
    def get_stockid_market_sh_sz(self):
        # for stockId in self.stockDict["timeToMarket"]:
        for stockId in self.stockDict[pf.股票清单表头[1]]:
            # print(stockId)
            if self.stockDict[pf.股票清单表头[21]][stockId] == 0:
                market = 'SZ'
            else:
                market = 'SH'
            self.stock_id_market_sh_sz.append([stockId,market])

    #################################################
    # 从股票字典获取股票代码和交易市场
    #################################################
    def get_stockid_market(self):
        # for stockId in self.stockDict["timeToMarket"]:
        for stockId in self.stockDict[pf.股票清单表头[1]]:
            # print(stockId)
            self.stock_id_market.append([stockId, self.stockDict[pf.股票清单表头[21]][stockId]])

    #################################################
    # 从股票字典获取股票代码除去《总市值》为空的，也就是去除退市和未上市的股票id
    #################################################
    def getStockIdWithoutNone(self):
        # for stockId in self.stockDict["timeToMarket"]:
        for stockId in self.stockDict[pf.股票清单表头[1]]:
            # print(stockId)
            # print(pf.股票清单表头[16])
            # print(self.stockDict[pf.股票清单表头[16]][stockId])
            if self.stockDict[pf.股票清单表头[16]][stockId] != '-':
                self.stockIdListWithoutNone.append(str(stockId))
        self.stockIdListWithoutNone.sort()

    #################################################
    # 从股票字典获取股票代码获取《总市值》为空的，也就是获取退市和未上市的股票id
    #################################################
    def getStockIdWithNone(self):
        # for stockId in self.stockDict["timeToMarket"]:
        for stockId in self.stockDict[pf.股票清单表头[1]]:
            # print(stockId)
            # print(pf.股票清单表头[16])
            # print(self.stockDict[pf.股票清单表头[16]][stockId])
            if self.stockDict[pf.股票清单表头[16]][stockId] == '-':
                self.stockIdListWithNone.append(str(stockId))
        self.stockIdListWithNone.sort()



if __name__ == '__main__':
    aa = StockDict()
    # print(aa.stockDict)
    for stockId in aa.stockDict[pf.股票清单表头[1]]:
        print(stockId, aa.stockDict[pf.股票清单表头[1]][stockId])

    # for element in aa.stockIdList:
    #     print(element)
    #
    # for e in aa.stock_id_market:
    #     print(e)
    #
    # for e in aa.stock_id_market_sh_sz:
    #     print(e)
    #
    # print('退市和未上市股票清单')
    # for element in aa.stockIdListWithNone:
    #     #pass
    #     print(element)