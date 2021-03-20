from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.types import FLOAT

import pandas as pd

from 函数目录 import profile as pf
from 函数目录.function import checkAndCreateDir, check_file_exist


class 沪深港通持股数据入库():
    # 初始化
    def __init__(self):
        self.engine = create_engine('sqlite:///C:\sqlite3\hsgtcg.db')
        self.columns=['日期', '股票代码', '股票名称' , '持股数量', '持股市值', '持股数量占A股百分比', '当日收盘价', '当日涨跌幅']#采集的列

        self.base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        self.dirname_步骤一 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤一, pf.SEPARATOR)

        checkAndCreateDir(self.dirname_步骤一)

        self.dirname_步骤二 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.沪深港通持股, pf.SEPARATOR, pf.步骤二, pf.SEPARATOR)
        checkAndCreateDir(self.dirname_步骤二)

    def 获取数据(self):
        engine = create_engine('sqlite:///C:\sqlite3\hsgtcg.db')

        #dict_df_步骤一 = pd.read_excel(self.dirname_步骤一 + '1' + pf.Execl, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理

        dict_df_步骤二 = pd.read_excel(self.dirname_步骤二 + pf.步骤二 + pf.Execl, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理

        for k, v in dict_df_步骤二.items():
            print(k)
            try:
                #print(v)
                #print(v.info())
                #v.to_sql('table' + k, engine, if_exists='replace', index_label='日期' ,  index=False, chunksize=1000,dtype={"持股数量占A股百分比": FLOAT(), '当日收盘价': FLOAT(), '当日涨跌幅': FLOAT()})
                v.to_sql('table' + k, engine, if_exists='replace',  index=False , chunksize=10000, dtype={"持股数量占A股百分比": FLOAT(), '当日收盘价': FLOAT(), '当日涨跌幅': FLOAT()})

                #v.to_sql('table' + k, engine, if_exists='replace', chunksize=1000,dtype={"持股数量占A股百分比": FLOAT(),'当日收盘价':FLOAT(),'当日涨跌幅':FLOAT()})
            except:
                print("有错")

    def 读取表里的数据(self):
        engine = create_engine('sqlite:///C:\sqlite3\hsgtcg.db')
        all_table_name = engine.execute("SELECT name FROM sqlite_master WHERE type ='table' ORDER BY name ").fetchall()
        print(all_table_name)
        print(len(all_table_name))
        for e in all_table_name:
            table_name = e[0]
            print(table_name)
            df1 = pd.read_sql_table(table_name, engine)
            print(df1)
            print(df1.info())

            dict_df_步骤一 = pd.read_excel(self.dirname_步骤一 + '2' + pf.Execl, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
            for k,v in dict_df_步骤一.items():


                df3 = pd.concat([v, df1]).drop_duplicates(subset=self.columns[0],
                                                           keep='first', inplace=False).reset_index(drop=True)

            df3.to_sql('table' + k, engine, if_exists='replace', index=False, chunksize=1000,
                     dtype={"持股数量占A股百分比": FLOAT(), '当日收盘价': FLOAT(), '当日涨跌幅': FLOAT()})

    def _获取表格里最大日期(self,table_name):
        try:
            max_date = self.engine.execute("SELECT max(日期) FROM "+ table_name).fetchall()[0][0]
            return max_date
        except:
            return None

    def _读取当天采集文件返回当天的一个字典(self):
        dict_df_步骤一 = pd.read_excel(self.dirname_步骤一 + pf.步骤一 + pf.Execl, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
        return dict_df_步骤一

    def 将字典的数据与数据库的数据进行合并存盘(self):
        dict_df = self._读取当天采集文件返回当天的一个字典()
        for k,v in dict_df.items():
            table_name = "table" + k
            max_date = self._获取表格里最大日期(table_name)
            if max_date is not None:
                pass
                #合并数据

            else:
                pass
                #直接保存数据


if __name__ == '__main__':
    print("start")
    #a = 沪深港通持股数据入库()
    #a.获取数据()
    #a.读取表里的数据()
    #a.获取表格里最大日期("table000001")