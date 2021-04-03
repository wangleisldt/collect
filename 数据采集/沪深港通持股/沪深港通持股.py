import requests
import json
import chardet
import pandas as pd
import time
import pickle
import os,shutil
from 函数目录 import profile as pf
from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getCurrentDate
from 数据采集.标准类.采集标准类 import 采集标准类
import joblib

class 沪深港通持股():
    # 初始化
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }#采集客户的的一些信息
        self.url = "http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?"#url链接
        self.columns=['日期', '股票代码', '股票名称' , '持股数量', '持股市值', '持股数量占A股百分比', '当日收盘价', '当日涨跌幅']#采集的列

        self.base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        self.dirname_步骤一 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤一, pf.SEPARATOR)
        checkAndCreateDir(self.dirname_步骤一)

        self.dirname_步骤二 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤二, pf.SEPARATOR)
        checkAndCreateDir(self.dirname_步骤二)

        self.dirname_步骤三 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤三, pf.SEPARATOR)
        checkAndCreateDir(self.dirname_步骤三)

        self.dirname_步骤四 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤四, pf.SEPARATOR)
        checkAndCreateDir(self.dirname_步骤四)

    def _将字典保存成Execl文件(self,dict,filename):
        with pd.ExcelWriter(filename) as writer:
            for e in sorted(dict.keys()):
                dict[e].to_excel(writer, sheet_name=e)
        #writer.save()
        #writer.close()

        '''
        #print(dict,filename)
        writer = pd.ExcelWriter(filename)  # 产生保存文件
        for e in sorted(dict.keys()):
            dict[e].to_excel( writer , sheet_name=e )
        writer.save()
        writer.close()
        '''


    def 根据全量股票进行获取(self,from_stockid="000000",sleep_stock_num= 500,sleep_sec = 5):
        # writer = pd.ExcelWriter(self.dirname_步骤一 + pf.步骤一 + getCurrentDate() + pf.Execl) #产生保存文件
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
                    df = self._获取数据(element)
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

        # writer.save()
        # writer.close()
        self._将字典保存成Execl文件(save_dict,self.dirname_步骤一 + pf.步骤一 + getCurrentDate() + pf.Execl)

        shutil.copyfile(self.dirname_步骤一 + pf.步骤一 + getCurrentDate() + pf.Execl, self.dirname_步骤一 + pf.步骤一  + pf.Execl)

        filename = '%s%s%s' % (self.dirname_步骤一 , pf.步骤一  , pf.GZ)
        joblib.dump(save_dict, filename, compress=3, protocol=None)
        filename = '%s%s%s%s' % (self.dirname_步骤一 , pf.步骤一 , getCurrentDate() , pf.GZ)
        joblib.dump(save_dict, filename, compress=3, protocol=None)

    def _产生url参数(self,stockid):
        pay_load = {
            'type': 'HSGTHDSTA',
            'token': '70f12f2f4f091e459a279469fe49eca5',
            'filter': '(SCODE=\'%s\')' % (stockid),
            'st': 'HDDATE',
            'sr': '- 1',
            'p': '1',
            'ps': '50',
            'js': '(x)',
            'rt': '51513209'
        }
        return pay_load

    def _处理返回List获取需要的字段(self,list_input):
        return_list = []
        for element in list_input:
            list = []
            list.append(element['HDDATE'].split('T')[0])
            list.append(element['SCODE'])
            list.append(element['SNAME'])
            list.append(round(element['SHAREHOLDSUM']))
            list.append(round(element['SHAREHOLDPRICE']))
            list.append(element['SHARESRATE'])
            list.append(element['CLOSEPRICE'])
            list.append(element['ZDF'])
            return_list.append(list)
        # 对第几列进行排序，现在是第4列
        def sort_col(elem):
            return elem[0]

        return_list.sort(key=sort_col, reverse=True)
        return return_list

    def _获取数据(self, stockid):
        """
            获取东方财富网沪深港通持股
            :param stockid: string e.g. 000860
            :param pause:
            :return:
            """
        # 获取数据
        instance = 采集标准类(url = self.url,params=self._产生url参数(stockid))
        list = instance._获取数据_json()

        #response = requests.get(self.url,headers=self.headers,params=self._产生url参数(stockid))
        #fencoding = chardet.detect(response.content)
        #content = response.content.decode(fencoding['encoding'],errors = 'ignore')
        #print(content)
        #list = json.loads(content)

        if list is not None:
            list = self._处理返回List获取需要的字段(list)
            if len(list) != 0:
                df = pd.DataFrame(list, columns=self.columns)
                #print(df)
                return df
            else:
                return None
        else:
            return None

    def 步骤一(self):
        dict_df_步骤一 = pd.read_excel(self.dirname_步骤一 + pf.步骤一 + pf.Execl, sheet_name=None,
                                    converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
        if check_file_exist(self.dirname_步骤二 , pf.步骤二 + pf.Execl):
            print(self.dirname_步骤二 + pf.步骤二 + pf.Execl)
            dict_df_步骤二 = pd.read_excel(self.dirname_步骤二 + pf.步骤二 + pf.Execl, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
            for k,v in dict_df_步骤一.items():
                print("开始合并处理：%s" % (k))
                if k in dict_df_步骤二.keys():
                    dict_df_步骤二[k] = pd.concat([v, dict_df_步骤二[k]]).drop_duplicates(subset=self.columns[0],
                                                                                keep='first', inplace=False).sort_values(by=['日期'], ascending=False).reset_index(drop=True)
                else:
                    dict_df_步骤二[k] = v
                #print(dict_df_步骤二[k])
            self._将字典保存成Execl文件(dict_df_步骤二 ,self.dirname_步骤二 + pf.步骤二 + getCurrentDate() + pf.Execl)
            self._将字典保存成Execl文件(dict_df_步骤二, self.dirname_步骤二 + pf.步骤二 + pf.Execl)
        else:
            self._将字典保存成Execl文件(dict_df_步骤一, self.dirname_步骤二 + pf.步骤二 + getCurrentDate() + pf.Execl)
            self._将字典保存成Execl文件(dict_df_步骤一, self.dirname_步骤二 + pf.步骤二 + pf.Execl)

    def 步骤二(self):
        dict_df_步骤二 = pd.read_excel(self.dirname_步骤二 + pf.步骤二 + pf.Execl, sheet_name=None,
                                    converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理

        dict = {1:'一天',5:'一周',10:'两周',20:'一月'}
        list = [self.columns[5] , self.columns[3]]

        for k,v in dict_df_步骤二.items():
            print("开始步骤二处理：%s" % (k))
            df = v
            s_持股数量 = df[list[1]] - df[list[1]][1:].reset_index(drop=True)
            for day in sorted(dict.keys()):
                out_list = []
                for i in range(s_持股数量.count()-day+1):
                    #print(s_持股数量[i:i+day]>0,s_持股数量[i:i+day]==0,s_持股数量[i:i+day]<0)
                    out_list.append([ s_持股数量[i:i+day][s_持股数量[i:i+day] > 0].count() ,s_持股数量[i:i+day][s_持股数量[i:i+day] == 0].count(),s_持股数量[i:i+day][s_持股数量[i:i+day] < 0].count() ])
                #print(out_list)
                df_add = pd.DataFrame(out_list, columns=[ list[1]+dict[day]+">0",list[1]+dict[day]+"=0",list[1]+dict[day]+"<0"] )
                for e in list:
                    #print(df[e])
                    #print(df[e][day:])
                    s = df[e] - df[e][day:].reset_index(drop=True)
                    dict_df_步骤二[k][e+dict[day]] = s
                #dict_df_步骤二[k][] = pd.concat([dict_df_步骤二[k],df_add]).reset_index(drop=True)
                dict_df_步骤二[k] = pd.concat([dict_df_步骤二[k], df_add]  , axis=1 )
                #print(dict_df_步骤二[k])

        self._将字典保存成Execl文件(dict_df_步骤二, self.dirname_步骤三 + pf.步骤三  + pf.Execl)
        #shutil.copyfile(self.dirname_步骤三 +  pf.步骤三 +  pf.Execl, self.dirname_步骤三 +  pf.步骤三 + getCurrentDate() + pf.Execl)

    def 步骤三(self):
        print("开始处理")
        dict_df_步骤三 = pd.read_excel(self.dirname_步骤三 + pf.步骤三 + pf.Execl, sheet_name=None,
                                    converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
        df = pd.DataFrame()
        for k,v in dict_df_步骤三.items():
            df = pd.concat([df,v.head(1)] )
        df = df[df[self.columns[0]]==df[self.columns[0]].max()].reset_index(drop=True)
        print("开始保存文件")
        df.to_excel(self.dirname_步骤四 + pf.步骤四 + df[self.columns[0]].max() + pf.Execl)


if __name__ == '__main__':
    a = 沪深港通持股()
    a.根据全量股票进行获取()
    #a.步骤一()
    #a.步骤二()
    #a.步骤三()

    filename = '%s%s%s' % (a.dirname_步骤一, pf.步骤一, pf.GZ)
    df = joblib.load(filename, mmap_mode=None)
    #print(df)
    #print(type(df))

    for k,v in df.items():
        print(k)
        #print(v.dtypes)
        # print(k, "------------", v)

