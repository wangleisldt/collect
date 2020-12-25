import pandas as pd
from 函数目录 import profile as pf
from 函数目录.function import  check_file_exist
from 函数目录.date import getCurrentDate
import joblib
from 数据采集.沪深港通持股.沪深港通持股 import 沪深港通持股

def 查看gz文件():
    沪深港通持股_instance = 沪深港通持股()
    dict_df_步骤二 = joblib.load(沪深港通持股_instance.dirname_步骤二 + pf.步骤二 + pf.GZ, mmap_mode=None)
    for k, v in dict_df_步骤二.items():
        print(k,v)
        if k == '002786':
            print(v)


def 步骤三():
    沪深港通持股_instance = 沪深港通持股()
    print("开始处理")
    #dict_df_步骤三 = pd.read_excel(沪深港通持股_instance.dirname_步骤三 + pf.步骤三 + pf.Execl, sheet_name=None,converters={1: str})  # 将股票代码其转换为字符串，这样就比较好处理
    dict_df_步骤三 = joblib.load(沪深港通持股_instance.dirname_步骤三 + pf.步骤三 + pf.GZ, mmap_mode=None)
    df = pd.DataFrame()
    for k,v in dict_df_步骤三.items():
        df = pd.concat([df,v.head(1)] )
    df = df[df[沪深港通持股_instance.columns[0]]==df[沪深港通持股_instance.columns[0]].max()].reset_index(drop=True)
    print("开始保存文件")
    df.to_excel(沪深港通持股_instance.dirname_步骤四 + pf.步骤四 + df[沪深港通持股_instance.columns[0]].max() + pf.Execl)


def 步骤二():
    DF_HEAD = 35
    沪深港通持股_instance = 沪深港通持股()
    dict_df_步骤二 = joblib.load(沪深港通持股_instance.dirname_步骤二 + pf.步骤二 + pf.GZ, mmap_mode=None)

    dict = {1:'一天',5:'一周',10:'两周',20:'一月'}
    list = [沪深港通持股_instance.columns[5] , 沪深港通持股_instance.columns[3]]

    for k,v in dict_df_步骤二.items():
        print("开始步骤二处理：%s" % (k))
        df = v

        #取前35行进行处理，这个数字可以调整
        df = df.head(DF_HEAD)

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

    filename = '%s%s%s' % (沪深港通持股_instance.dirname_步骤三, pf.步骤三, pf.GZ)
    joblib.dump(dict_df_步骤二, filename, compress=3, protocol=None)
    #沪深港通持股_instance._将字典保存成Execl文件(dict_df_步骤二, 沪深港通持股_instance.dirname_步骤三 + pf.步骤三  + pf.Execl)
    #shutil.copyfile(self.dirname_步骤三 +  pf.步骤三 +  pf.Execl, self.dirname_步骤三 +  pf.步骤三 + getCurrentDate() + pf.Execl)


def 步骤一():
    沪深港通持股_instance = 沪深港通持股()
    filename = '%s%s%s' % (沪深港通持股_instance.dirname_步骤一, pf.步骤一, pf.GZ)
    dict = joblib.load(filename, mmap_mode=None)

    if check_file_exist(沪深港通持股_instance.dirname_步骤二, pf.步骤二 + pf.GZ):
        print(沪深港通持股_instance.dirname_步骤二 + pf.步骤二 + pf.GZ)
        dict_df_步骤二 = joblib.load(沪深港通持股_instance.dirname_步骤二 + pf.步骤二 + pf.GZ, mmap_mode=None)
        for k, v in dict.items():
            print("开始合并处理：%s" % (k))
            if k in dict_df_步骤二.keys():
                dict_df_步骤二[k] = pd.concat([v, dict_df_步骤二[k]]).drop_duplicates(subset=沪深港通持股_instance.columns[0],
                                                                                keep='first',
                                                                                inplace=False).sort_values(by=['日期'],
                                                                                                           ascending=False).reset_index(
                    drop=True)
            else:
                dict_df_步骤二[k] = v
    else:
        dict_df_步骤二 = dict

    filename = '%s%s%s' % (沪深港通持股_instance.dirname_步骤二 , pf.步骤二 ,  pf.GZ)
    joblib.dump(dict_df_步骤二, filename, compress=3, protocol=None)
    filename = '%s%s%s%s' % (沪深港通持股_instance.dirname_步骤二, pf.步骤二, getCurrentDate() ,pf.GZ)
    joblib.dump(dict_df_步骤二, filename, compress=3, protocol=None)

    沪深港通持股_instance._将字典保存成Execl文件(dict_df_步骤二, 沪深港通持股_instance.dirname_步骤二 + pf.步骤二 + pf.Execl)



if __name__ == '__main__':
    步骤一()
    #查看gz文件()
    #步骤二()
    #步骤三()
