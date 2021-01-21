import 交易数据.RehabilitationOfHistoricalData as rohd

if __name__ == '__main__':
    #获取历史交易数据，一般使用后复权，设置为False，如果需要前复权则设置为True
    #rohd.getStockYearData(2018,qfq=False)
    rohd.getStockYearData(2020, qfq=True)
