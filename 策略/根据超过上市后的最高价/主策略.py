from 策略.根据超过上市后的最高价.获取股票清单 import 获取股票清单,获取股票清单字典
from 策略.根据超过上市后的最高价.获取股票上市n天以后的最高价格 import 根据股票代码获取上市日期,获取股票上市n天以后的最高价格,给定一天获取这天以后的超过这个价格的日期及价格
from 函数目录 import profile as pf
from 交易数据.CalculateStockPriceDifference import 给定某天获取n天以后的股票价格

def 主策略():
    stock_list = 获取股票清单()
    stock_dict = 获取股票清单字典()

    for element in stock_list:
        time_to_market = 根据股票代码获取上市日期(element, stock_dict)
        #print(element,time_to_market)
        if time_to_market != 0 and time_to_market >= 20100101:
            top_price_date, top_price = 获取股票上市n天以后的最高价格(element,time_to_market,230)
            if top_price != 0:
                #print(top_price_date,top_price)
                date,price = 给定一天获取这天以后的超过这个价格的日期及价格(element, top_price_date, top_price, type=pf.Hfq)
                #print("%s-%s-%s-%s-%s" % (element,top_price_date, top_price ,price,date))

                if price != top_price:
                    #print(element, time_to_market, top_price_date, top_price, date , price)
                    后面几天的日期,后面几天的价格, 长度, 返回状态 = 给定某天获取n天以后的股票价格(element, date, 22, type=pf.Hfq)
                    后22天的百分比 = round((后面几天的价格 - price) / price*100)
                    后面几天的日期, 后面几天的价格, 长度, 返回状态 = 给定某天获取n天以后的股票价格(element, date, 44, type=pf.Hfq)
                    后44天的百分比 = round((后面几天的价格 - price) / price*100)
                    后面几天的日期, 后面几天的价格, 长度, 返回状态 = 给定某天获取n天以后的股票价格(element, date, 66, type=pf.Hfq)
                    后66天的百分比 = round((后面几天的价格 - price) / price*100)
                    后面几天的日期, 后面几天的价格, 长度, 返回状态 = 给定某天获取n天以后的股票价格(element, date, 132, type=pf.Hfq)
                    后132天的百分比 = round((后面几天的价格 - price) / price*100)

                    print("%s#%s#%s#%s#%s#%s#%s#%s#%s#%s" % (element, time_to_market, top_price_date, top_price, date, price,后22天的百分比,后44天的百分比,后66天的百分比,后132天的百分比))

if __name__ == '__main__':
    主策略()

