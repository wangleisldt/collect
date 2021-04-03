import requests
import json
import chardet
from 函数目录 import profile as pf
import time
import random
from 数据采集.股票清单.股票清单获取 import StockDict

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
]

class 采集标准类():
    # 初始化
    def __init__(self,url,params=None,proxies=pf.proxies,timeout =10):
        self.headers = {
            # 'User-Agent': random.choice(USER_AGENT_LIST),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }#采集客户的的一些信息
        self.url = url#url链接
        self.params = params
        self.proxies=proxies
        self.timeout=timeout

    def _获取数据_json(self):
        try:
            response = requests.get(self.url,headers=self.headers,params=self.params,proxies=self.proxies,timeout=self.timeout)
            #print(response.url)
            fencoding = chardet.detect(response.content)
            content = response.content.decode(fencoding['encoding'],errors = 'ignore')
            #print(content)
            return_json = json.loads(content)
            return return_json
        except:
            return None

    def _获取数据(self):
        try:
            response = requests.get(self.url,headers=self.headers,params=self.params,proxies=self.proxies,timeout=self.timeout)
            #print(response.url)
            fencoding = chardet.detect(response.content)
            content = response.content.decode(fencoding['encoding'],errors = 'ignore')
            return content
        except:
            return None

    def _获取数据_text(self):
        try:
            response = requests.get(self.url,headers=self.headers,params=self.params,proxies=self.proxies,timeout=self.timeout)
            content = response.text
            return content
        except:
            return None

    def 获取每个数据(self,element):
        pass

    def 根据全量股票进行获取(self,from_stockid="000000",sleep_stock_num= 500,sleep_sec = 5):
        #初始化全部股票代码
        stockListInstance = StockDict()
        #对每个股票代码进行处理
        count = 0
        save_dict = {}
        for element in stockListInstance.stockIdList:
            if count == sleep_stock_num:
                print('网页查询了%s个股票等待%s秒！' % (sleep_stock_num,sleep_sec))
                time.sleep(sleep_sec)
                count = 0
            else:
                count = count + 1
            try:
                if element >= from_stockid:
                    print("开始获取%s" %element)
                    df = self._获取每个数据(element)
                    time.sleep(1)
                    if df is not None:
                        # df.to_excel(writer, sheet_name=element)
                        save_dict[element] = df
                    else:
                        print("%s无相关数据。" % element)
                else :
                    print("%s已获取过。" %element)
            except:
                print("获取%s失败################################################"  %element )

            return save_dict

if __name__ == '__main__':
    pass