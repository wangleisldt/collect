import requests
import json
import chardet
from 函数目录 import profile as pf

class 采集标准类():
    # 初始化
    def __init__(self,url,params=None,proxies=pf.proxies,timeout =10):
        self.headers = {
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

if __name__ == '__main__':
    pass