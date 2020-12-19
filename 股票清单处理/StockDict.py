import pickle

from 函数目录 import profile as pf


class StockDict:
    # 初始化
    def __init__(self):
        self.filename = '%s%s%s' % (pf.GLOBAL_PATH + pf.SEPARATOR + pf.FUNDAMENTAL_DATA + pf.SEPARATOR + pf.StockList + pf.SEPARATOR, pf.StockListFilename, pf.PklFile)
        self.stockDict = {}
        self.stockIdList = []
        self.getStockFromFileToDict()
        self.getStockId()

    #################################################
    # 获取股票清单到Dict(类初始化时自动加载)
    #################################################
    def getStockFromFileToDict(self):
        pklFile = open( self.filename , 'rb')
        self.stockDict = pickle.load(pklFile)
        pklFile.close()

    #################################################
    # 从股票字典获取股票代码
    #################################################
    def getStockId(self):
        for stockId in self.stockDict[pf.股票清单表头[1]]:
            self.stockIdList.append(stockId)
            print(stockId, self.stockDict[pf.股票清单表头[1]][stockId])
        #for stockId in self.stockDict["timeToMarket"]:
            #self.stockIdList.append(stockId)

if __name__ == '__main__':
    aa = StockDict()
    #for stockId in aa.stockDict["timeToMarket"]:
        #print(stockId,aa.stockDict["timeToMarket"][stockId])

    for element in aa.stockIdList:
        print(element)

    for k,v in aa.stockDict.items():
        print(k,"----------",v)

