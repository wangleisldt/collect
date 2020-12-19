from 交易数据.CalculateStockPriceDifference import 获取给定时间段的股票最高价
from 函数目录 import profile as pf, date
import xlrd

def 根据股票代码获取上市日期(stock_id,stock_dict):
    return stock_dict.stockDict["timeToMarket"][stock_id]

def 获取股票上市n天以后的最高价格(stock_id,time_to_market,n_day):
    top_price_date, top_price = 获取给定时间段的股票最高价(stock_id,str(time_to_market),n_day, type=pf.Hfq)
    return top_price_date, top_price

def 给定一天获取这天以后的超过这个价格的日期及价格(stock_id,start_date,price,type=pf.Hfq):
    #print(stock_id,start_date)
    start_date = date.后几天(start_date,1)
    year, month, day = start_date[0:4], start_date[4:6], start_date[6:8]
    top_price = price
    top_price_date = ""
    while year != str(date.getCurrentYear() + 1) and top_price == price:
        #print(stock_id, start_date, top_price )
        top_price_date,top_price = 读取比较某年交易数据(stock_id, start_date, top_price, top_price_date, type)
        #print(stock_id, start_date, top_price,top_price_date)

        if top_price_date == "":
            year = str(int(year) + 1)
            start_date = "%s%s%s" % (year, "01", "01")
            #print(top_price , top_price_date)

    top_price_date = "%s%s%s" % (top_price_date[0:4], top_price_date[5:7], top_price_date[8:10])
    return top_price_date, top_price

def 读取比较某年交易数据(stock_id, start_date, top_price, top_price_date, type=pf.Hfq):
    #print(type(top_price))
    try:
        year, month, day = start_date[0:4], start_date[4:6], start_date[6:8]
        date = "%s-%s-%s" % (year ,month,day)
        # 打开文件，读取每一行，每一列
        dirBase = pf.GLOBAL_PATH + pf.SEPARATOR + pf.TransactionData + pf.SEPARATOR + pf.HistoryData + pf.SEPARATOR
        filename = dirBase + type + pf.SEPARATOR + year + pf.SEPARATOR + stock_id + pf.Execl
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        rows = sheet.nrows
        for i in range(rows):
            if i != 0:
                row = sheet.row_values(i)
                if row[1] >= date:
                    #print(row)
                    if top_price < row[3]:
                        top_price = row[3]
                        top_price_date = row[1]
                        workbook.release_resources()
                        del workbook
                        return top_price_date,top_price
        workbook.release_resources()
        del workbook
        return top_price_date,top_price
    except:
        return top_price_date,top_price


if __name__ == '__main__':
    #stock_dict = 获取股票清单()
    #aa = 根据股票代码获取上市日期("600663", stock_dict)
    #print(获取股票上市n天以后的最高价格("600663", "20100518",20))

    date,price = 给定一天获取这天以后的超过这个价格的日期及价格("300745", "20180529", 80.41)
    print(date)