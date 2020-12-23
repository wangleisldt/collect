from 函数目录.function import checkAndCreateDir, file_List_Func
import 函数目录.profile as pf
import pandas as pd
import joblib
from 数据采集.沪深港通持股.沪深港通持股 import 沪深港通持股

Path = "/home/wangleisldt/collect_data/基本面数据/沪深港通持股/历史数据/2019/"
OUTPUT_PATH = '/home/wangleisldt/collect_data/基本面数据/沪深港通持股/历史数据/'
OUTPUT_FILENAME='2019'

def 格式转换(Path = Path):
    #将execl文件转换为gz文件。
    file_list = file_List_Func(Path)
    for filename  in file_list:
        firstname = filename.split(".")[0]
        print(firstname)
        dict = pd.read_excel(Path+filename, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
        filename_save = '%s%s%s' % (Path, firstname, pf.GZ)
        joblib.dump(dict, filename_save, compress=3, protocol=None)

def 文件合并(path = Path ,output_filename=OUTPUT_FILENAME ):
    沪深港通持股_instance = 沪深港通持股()
    file_list = sorted(file_List_Func(path))
    output_dict_df = {}

    for e in file_list:
        #print("开始处理：", e)
        firstname , extend  = e.split(".")
        if extend == pf.GZ[1:]:
            print("开始处理：", e)
            #print(firstname, extend)
            filename = '%s%s' % (path, e)
            dict_df = joblib.load(filename, mmap_mode=None)
            for k, v in dict_df.items():
                if k in output_dict_df.keys():
                    output_dict_df[k] = pd.concat([v, output_dict_df[k]]).drop_duplicates(subset=沪深港通持股_instance.columns[0],
                                                                                    keep='first',
                                                                                    inplace=False).sort_values(
                        by=['日期'],
                        ascending=False).reset_index(
                        drop=True)
                else:
                    output_dict_df[k] = v

    print("开始保存gz文件：")
    filename = '%s%s%s' % (OUTPUT_PATH,output_filename, pf.GZ)
    joblib.dump(output_dict_df, filename, compress=3, protocol=None)

    print("开始保存execl文件：")
    filename = '%s%s%s' % (OUTPUT_PATH, output_filename, pf.Execl)
    沪深港通持股_instance._将字典保存成Execl文件(output_dict_df, filename)

if __name__ == '__main__':
    #格式转换()
    文件合并()

