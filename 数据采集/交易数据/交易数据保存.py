from 函数目录 import profile as pf
from 函数目录.function import check_file_exist,save_file_dataframe_to_execl
import pandas as pd
import pickle

base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.交易数据)
dirname = "%s%s%s%s%s" % (base_dir_name, pf.SEPARATOR, pf.历史行情, pf.SEPARATOR, pf.后复权)

def 保存交易数据(stockid,df):
    #修改字段类型
    df[[  '开盘', '收盘', '最高', '最低',  '成交额','振幅', '涨跌幅', '涨跌额', '换手率']] = df[[   '开盘', '收盘', '最高', '最低',  '成交额','振幅', '涨跌幅', '涨跌额', '换手率']].astype(float)
    df[['成交量']] = df[['成交量']].astype(int)

    full_file_name = '%s%s%s%s' % (dirname, pf.SEPARATOR, stockid, pf.PklFile_GZ)
    if check_file_exist(dirname, stockid+ pf.PklFile_GZ):
        print("存在文件，进行合并去重。")
        #读取目录中的文件删除最后一行，与新df做合并去重排序等
        df_file = pd.read_pickle(full_file_name)
        df_file = df_file.drop(df_file.tail(1).index)#删除最后一行
        #print(df_file.dtypes)
        #print(df.dtypes)
        new_df = pd.concat([df_file , df]).drop_duplicates(keep='first', inplace=False).sort_values(by=['日期'], ascending=True).reset_index(drop=True)#合并去重
        new_df.to_pickle(full_file_name)
        print("成功保存文件：%s" % (full_file_name))
        #print(new_df)
    else:
        print("不存在文件。")
        df.to_pickle(full_file_name)
        print("成功保存文件：%s" % (full_file_name))

if __name__ == '__main__':
    full_file_name = '%s%s%s%s' % (dirname,pf.SEPARATOR,'000001', pf.PklFile_GZ)
    df = pd.read_pickle(full_file_name)
    print(df)
    print(df.dtypes)