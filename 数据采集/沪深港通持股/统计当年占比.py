import pandas as pd
from 函数目录 import profile as pf
from pathlib import Path
import joblib
# from 数据采集.沪深港通持股.沪深港通持股 import 沪深港通持股

def 处理整个文件(filename=None):
    if filename is None:
        filename = Path(pf.GLOBAL_PATH, pf.FUNDAMENTAL_DATA, pf.沪深港通持股, pf.步骤二, pf.步骤二+ pf.GZ)

    # 沪深港通持股_instance = 沪深港通持股()
    dict_df = joblib.load(filename , mmap_mode=None)

    return_df = None
    for k,v in dict_df.items():
        print("开始处理：%s" % (k))
        df = v
        # print(df)
        df = 处理单个dataframe(df)
        if df is None:
            continue
        elif return_df is None:
            df = df.reset_index()
            return_df = df
        else:
            df = df.reset_index()
            return_df = pd.concat([return_df,df])
        # print(return_df)
        # print(df)
        # joblib.dump(df, 沪深港通持股_instance.dirname_步骤二 + "aaa" + pf.GZ, compress=3, protocol=None)
        # exit()
    return_df = return_df.set_index(keys=['股票代码', '股票名称'])
    return return_df

def 保存dataframe(df):
    filename = Path(pf.GLOBAL_PATH, pf.FUNDAMENTAL_DATA, pf.沪深港通持股,  "当年情况文件" +  pf.Execl)
    df.to_excel(filename)

def 处理单个dataframe(df):
    df['date2'] = pd.to_datetime(df['日期'], infer_datetime_format=True)#将字符串转换为日期
    df['YearMonth'] = df['date2'].map(lambda x: x.strftime('%Y-%m'))
    df = df.groupby(['YearMonth','股票代码','股票名称'])['持股数量占A股百分比'].mean()
    # print(df)
    df = pd.DataFrame(df).reset_index()
    # print(df)
    df.columns = ['日期', '股票代码', '股票名称','持股数量占A股百分比-月平均']
    df1 = df[['股票代码', '股票名称']]
    df1= df1.drop_duplicates(keep='first')
    if len(df1) > 1:
        df1= df1.head(1)
        return None
    if len(df1) < 1:
        return None
    # print(df1)
    df = df[['日期','持股数量占A股百分比-月平均']]
    # df = df.set_index(keys=['股票代码', '股票名称'])
    df = df.set_index(keys=['日期'])
    # print(df)
    # print("$$$$$$$$$$$$$$$$$$$$")
    df = df.T
    # print(df)
    # print("$$$$$$$$$$$$$$$$$$$$")
    # print(df.info())
    df = df.reset_index()
    df = pd.concat([df,df1],axis=1)
    # print(df)
    df = df.drop('index', 1)
    df = df.set_index(keys=['股票代码','股票名称'])
    # print(df)
    return df

if __name__ == '__main__':
    filename = None
    # filename = Path(pf.GLOBAL_PATH, pf.FUNDAMENTAL_DATA, pf.沪深港通持股, "历史数据","2020" + pf.GZ)
    df = 处理整个文件(filename)
    print(df)
    保存dataframe(df)