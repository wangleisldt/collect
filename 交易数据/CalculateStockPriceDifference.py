import xlrd

from 函数目录 import profile as pf, date
from 函数目录 import profile as pf
from 函数目录 import date as dt


def getPriceFromExecl(StockId,YearMonth,Type=pf.Hfq,PriceCount = 3):
    try:
        # 打开文件，读取每一行，每一列
        dirBase = pf.GLOBAL_PATH + pf.SEPARATOR + pf.TransactionData + pf.SEPARATOR + pf.HistoryData + pf.SEPARATOR
        filename = dirBase + Type + pf.SEPARATOR + YearMonth[0:4] + pf.SEPARATOR +StockId + pf.Execl
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        rows = sheet.nrows
        price = 0
        count = PriceCount
        for i in range(rows):
            if i != 0:
                row = sheet.row_values(i)
                if str(row[1][0:4])+str(row[1][5:7]) == YearMonth:
                    if count > 0:
                        count = count -1
                        price = round(price + round(row[3], 2), 2)
        if count == 0 :
            return round(price/PriceCount,2)
        else:
            return 0
    except:
        return 0


#################################################
# 计算股票获利百分比
#################################################
def calculateStockPriceDifference(StockId,FromYearMonth,LengthMonth,Type=pf.Hfq,PriceCount=3):
    toYearMonth = date.getYearMonthFromMonthLength(FromYearMonth, LengthMonth)
    priceBegin = getPriceFromExecl(StockId, FromYearMonth, Type=Type, PriceCount = PriceCount)
    priceEnd = getPriceFromExecl(StockId, toYearMonth, Type=Type, PriceCount=PriceCount)
    #返回增长率
    if priceBegin!=0 and priceEnd !=0:
        return True,round((priceEnd-priceBegin)/priceBegin*100 , 5),FromYearMonth,toYearMonth
    else:
        return False,0,FromYearMonth,toYearMonth

#################################################
# 读取某月数据
#################################################
def 读取比较某月交易数据(stock_id, start_date, length , top_price , top_price_date,type=pf.Hfq):
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
                if row[1] >= date and length !=0:
                    length = length -1
                    #print(row)
                    if top_price <= row[3]:
                        top_price = row[3]
                        top_price_date = row[1]
        workbook.release_resources()
        del workbook
        return top_price,length,top_price_date
    except:
        return top_price,length,top_price_date

#################################################
# 获取给定起始时间开始，固定日期，股票收盘最高价
#################################################
def 获取给定时间段的股票最高价(stock_id,start_date,length,type=pf.Hfq):
    try:
        year,month,day = start_date[0:4],start_date[4:6],start_date[6:8]
        top_price = 0
        top_price_date = ""
        while length != 0 and year != str(dt.getCurrentYear()+1):
            #print(stock_id, start_date, length , top_price , type)
            top_price , length , top_price_date = 读取比较某月交易数据(stock_id, start_date, length , top_price ,top_price_date ,type)
            year = str(int(year)+1)
            start_date = "%s%s%s" % (year, "01", "01")
            #print(top_price , length , top_price_date)
            top_price_date_return = "%s%s%s" % (top_price_date[0:4],top_price_date[5:7],top_price_date[8:10])
        return top_price_date_return,top_price
    except:
        return "",0


#################################################
# 给定某天获取当月n天以后的股票价格
#################################################
def 给定某天获取当年n天以后的股票价格(stock_id,start_date,length,type=pf.Hfq):
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
            row = sheet.row_values(i)
            if row[1] >= date and i != 0 and length !=-1 :
                #row = sheet.row_values(i)
                length = length -1
                price = row[3]
                date = row[1]
        workbook.release_resources()
        del workbook
        return date,price,length+1, True
    except:
        return "",0,0, False


#################################################
# 给定某天获取n天以后的股票价格
#################################################
def 给定某天获取n天以后的股票价格(stock_id,start_date,length,type=pf.Hfq):
    try:
        year,month,day = start_date[0:4],start_date[4:6],start_date[6:8]
        status = True
        while length >= 0 and year != str(dt.getCurrentYear() + 1) and status == True:
            day, price, length, status = 给定某天获取当年n天以后的股票价格(stock_id, start_date, length, type=pf.Hfq)
            if length != 0:
                year = str(int(year) + 1)
                start_date = "%s%s%s" % (year, "01", "01")
            else:
                length = length -1
        return day, price, length, status
    except:
        return "", 0, 0, False


if __name__ == '__main__':
    b = calculateStockPriceDifference("600900", "201408",36)
    #print(b)

    top_price_date, top_price = 获取给定时间段的股票最高价("601360", "20120116", 150, type=pf.Hfq)
    #print(top_price_date, top_price)

    date, price, length ,status= 给定某天获取当年n天以后的股票价格("600663", "20170504", 0, type=pf.Hfq)

    print(date, price, length,status)

    date, price, length, status = 给定某天获取n天以后的股票价格("600663", "20130504", 990, type=pf.Hfq)

    print(date, price, length, status)