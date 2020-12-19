
from 数据采集.股票清单.股票清单获取 import StockDict

def 获取股票清单():
    stock_list_instance = StockDict()
    return stock_list_instance.stockIdList

def 获取股票清单字典():
    stock_dict_instace = StockDict()
    return stock_dict_instace

if __name__ == '__main__':
    print(获取股票清单())