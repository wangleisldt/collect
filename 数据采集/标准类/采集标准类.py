import requests
import json
import chardet
from 函数目录 import profile as pf

from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getCurrentDate

def 请求数据(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    fencoding = chardet.detect(response.content)
    content = response.content.decode(fencoding['encoding'], errors='ignore')[13:]
    #print(content)
    return content

def 请求数据_原始(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    fencoding = chardet.detect(response.content)
    content = response.content.decode(fencoding['encoding'], errors='ignore')
    #print(content)
    return content

class 采集标准类():
    # 初始化
    def __init__(self,url,params=None,proxies=pf.proxies):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }#采集客户的的一些信息
        self.url = url#url链接
        self.params = params
        self.proxies=proxies

    def _获取数据_json(self):
        response = requests.get(self.url,headers=self.headers,params=self.params,proxies=self.proxies)
        #print(response.url)
        fencoding = chardet.detect(response.content)
        content = response.content.decode(fencoding['encoding'],errors = 'ignore')
        #print(content)
        return_json = json.loads(content)
        return return_json

if __name__ == '__main__':
    pass
    #print(dict)