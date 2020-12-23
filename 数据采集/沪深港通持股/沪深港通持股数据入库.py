from sqlalchemy import create_engine
from sqlalchemy.types import FLOAT

import pandas as pd

from 函数目录 import profile as pf
from 函数目录.function import checkAndCreateDir, file_List_Func


class 沪深港通持股数据入库():
    # 初始化
    def __init__(self):
        self.engine = create_engine(pf.DATABASE_STRING_沪深港通持股)
        self.columns=['日期', '股票代码', '股票名称' , '持股数量', '持股市值', '持股数量占A股百分比', '当日收盘价', '当日涨跌幅']#采集的列

        self.base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        self.dirname_步骤一 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤一, pf.SEPARATOR)

        checkAndCreateDir(self.dirname_步骤一)

        self.dirname_步骤二 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤二, pf.SEPARATOR)
        checkAndCreateDir(self.dirname_步骤二)

    def 扫描目录将目录中的文件入库(self,path):
        file_list = file_List_Func(path)

        for e in file_list:
            print("开始处理：", path + pf.SEPARATOR + e)
            dict_df = pd.read_excel( path + pf.SEPARATOR +e , sheet_name=None,converters={1: str})
            self._将字典的数据与数据库的数据进行合并存盘(dict_df)

    def 将当天数据与数据库的数据进行合并存盘(self):
        dict_df = self._读取当天采集文件返回当天的一个字典()
        self._将字典的数据与数据库的数据进行合并存盘(dict_df)

    def 读取表里的数据(self):
        engine = self.engine
        all_table_name = engine.execute("SELECT name FROM sqlite_master WHERE type ='table' ORDER BY name ").fetchall()
        print(all_table_name)
        print(len(all_table_name))
        for e in all_table_name:
            table_name = e[0]
            print(table_name)
            df1 = pd.read_sql_table(table_name, engine)
            print(df1)
            print(df1.info())

    def _获取表格里最大日期(self,table_name):
        try:
            max_date = self.engine.execute("SELECT max(日期) FROM "+ table_name).fetchall()[0][0]
            return max_date
        except:
            return None

    def _获取表格里某个表的数据(self,table_name):
        try:
            data = pd.read_sql_table(table_name, self.engine)
            return data
        except:
            return None

    def _读取当天采集文件返回当天的一个字典(self):
        dict_df_步骤一 = pd.read_excel(self.dirname_步骤一 + pf.步骤一 + pf.Execl, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
        return dict_df_步骤一

    def _将字典的数据与数据库的数据进行合并存盘(self,dict_df):
        #dict_df = self._读取当天采集文件返回当天的一个字典()
        for k,v in dict_df.items():
            print("开始处理：%s" %k )
            table_name = "table" + k
            max_date = self._获取表格里最大日期(table_name)
            if max_date is not None:
                #print("已有数据")

                #选取采集数据中大于表格中最大一天的数据
                #v = v.loc[v['日期'] > max_date]
                #print(v)

                #选取表格里的所有数据
                df = self._获取表格里某个表的数据(table_name)
                # print(df)

                #对两个数据进行合并
                df_concat = pd.concat([v, df]).drop_duplicates(subset=self.columns[0],keep='first', inplace=False).sort_values(by=['日期'], ascending=False).reset_index(drop=True)
                # print(df_concat)
                try:
                    if len(df_concat) != len(df):
                        df_concat.to_sql('table' + k, self.engine, if_exists='replace', index=False, chunksize=1000,dtype={"持股数量占A股百分比": FLOAT(), '当日收盘价': FLOAT(), '当日涨跌幅': FLOAT()})
                    else:
                        print("与表里数据一样！")
                except:
                    print("合并出错")

            else:
                print("没有数据")
                #直接保存数据
                try:
                    v.to_sql('table' + k, self.engine, if_exists='replace', index=False, chunksize=1000,
                                 dtype={"持股数量占A股百分比": FLOAT(), '当日收盘价': FLOAT(), '当日涨跌幅': FLOAT()})
                except:
                    print("合并出错")



if __name__ == '__main__':
    a = 沪深港通持股数据入库()

    #a.将当天数据与数据库的数据进行合并存盘()
    #a.扫描目录将目录中的文件入库("/home/wangleisldt/collect_data/基本面数据/沪深港通持股/步骤一")

    #a.读取表里的数据()