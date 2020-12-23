from 函数目录 import profile as pf
from 函数目录.function import file_List_Func
import pickle
import pandas as pd
from 函数目录.date import getYearMonthFromMonthLength


class 上市公司调研情况月度数据处理():
    # 初始化
    def __init__(self):

        self.dict = {}
        self.returnDict = {}

        # 产生需要打开的目录
        self.base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
        self.dirname_原始 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR)
        self.dirname_单个汇总 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.单个汇总, pf.SEPARATOR)
        self.dirname_汇总数据 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.汇总数据, pf.SEPARATOR)
        self.dirname_展现数据 = "%s%s%s%s%s%s" % (
            self.base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.展现数据, pf.SEPARATOR)

    def 数据汇总_步骤一(self):
        writer = pd.ExcelWriter(self.dirname_单个汇总 + pf.投资者关系活动记录表 + pf.单个汇总 + pf.Execl)  # 产生保存文件

        dict_df_步骤一 = pd.read_excel(self.dirname_原始 + pf.投资者关系活动记录表 +pf.Execl, sheet_name=None,
                                    converters={0: str})  # 将其转换为字符串，这样就比较好处理
        for k, v in dict_df_步骤一.items():
            df = v


            '''
            #a = df.str.startwith('2018-07')
            #a = df[['股票代码']]
            # a = df.values
            a = df.iloc[1,5]
            a = df.loc[1]
            a = df.loc[1:2,3:5]
            a = df.iloc[1:2, 3:5]
            a = df.values
            #a = df[df[3,1:6] == '2018-06']
            #a = df.values
            #print(df)
            #print(df.dtypes)
            #print(df)
            #print(df.groupby([0,1,5]).sum())
            #print(df.dtypes)

            #print(df[3].str.slice(0,7))
            #print(df[3])
            '''

            '''
            原始数据类似下面的结构
                     0     1  2        3        4       5
0   000001  平安银行  1  2018-06  2018-08  特定对象调研
1   000001  平安银行  1  2018-05  2018-08      其他
2   000001  平安银行  1  2018-04  2018-08  特定对象调研
3   000001  平安银行  1  2018-02  2018-04  特定对象调研
4   000001  平安银行  1  2018-01  2018-04  特定对象调研
'''
            # print(df)

            # 对第三列进行字符串截取，并替换df

            df.loc[:, '调研时间'] = df['调研时间'].str.slice(0, 7)
            # 对第四列进行字符串截取，并替换df
            df.loc[:, '公告日期'] = df['公告日期'].str.slice(0, 7)

            # print(df)
            # 做groupby,其中reset_index的目的为将相同的数据显示成不同的行中
            '''
            使用reset_index的结果
                     0     1        3  2
34  000001  平安银行  2018-06  1
33  000001  平安银行  2018-05  1
32  000001  平安银行  2018-04  1
31  000001  平安银行  2018-02  1
'''

            '''
            不使用reset_index的结果
            0      1    3  2       
000001 平安银行 2018-06  1
            2018-05  1
            2018-04  1
            2018-02  1
            2018-01  2

            '''

            # print(df)

            # 将接待方式为Nan的替换为空格，否则坐group的时候会报错。  groupby不能对空做group
            # df=df.fillna({'接待方式': "空"})
            df = df.fillna("空")
            # df = df.groupby([3]).sum()
            df = df.groupby(['股票代码', '股票名称', '调研时间']).sum().reset_index()
            # print(df)

            # 做一次排序操作
            # df = df.sort_values(by= 3,ascending=False)
            df = df.sort_index(axis=0, ascending=False)
            # print(df)
            df.columns = [0, 1, 2, 3]

            #print(df)
            print("汇总了%s。" % k)

            df.to_excel(writer, sheet_name=k)

        writer.save()
        writer.close()
        print("结束预处理汇总。")

    def 数据汇总_步骤二(self, year_month):
        dict_df_步骤二 = pd.read_excel(self.dirname_单个汇总 + pf.投资者关系活动记录表 + pf.单个汇总 + pf.Execl, sheet_name=None,
                                    converters={0: str})  # 将其转换为字符串，这样就比较好处理



        # 输出的list
        output_list = []

        for k, v in dict_df_步骤二.items():

            print("开始汇总股票：%s" %  k)
            df = v
            # print(df)
            # print(df.dtypes)
            year, month = str(year_month)[0:4], str(year_month)[4:6]

            # 选择需要的行，其中第二列的日期类似为“2018-08”
            df = df.ix[df[2] == year + "-" + month]

            if df.empty is False:
                # 如果非空则将数据保存到list
                output_list.append(df.values.tolist()[0])

        # 对结果进行排序
        output_list = sorted(output_list, key=lambda dycs: dycs[3], reverse=True)
        for element in output_list:
            print(element)

        # 将结果保存为execl文件
        filename = self.dirname_汇总数据 + str(year_month) + pf.Execl
        df = pd.DataFrame(output_list, columns=['股票代码', '股票名称', '调研时间', '调研次数'])
        df.to_excel(filename)

    def 数据展示(self, from_year_month, length):

        print("开始进行数据展示文件生成。")
        # 打开根据年月打开目录读取里面的文件
        # 读取文件，将每个文件的df存到dict中，并将调研次数这列改名为年月
        output_dict = {}
        for i in range(length):
            year_month = getYearMonthFromMonthLength(str(from_year_month), i)
            filename = self.dirname_汇总数据 + str(year_month) + pf.Execl
            df = pd.read_excel(filename, converters={0: str})  # 将其转换为字符串，这样就比较好处理
            df = df[['股票代码', '股票名称', '调研次数']]
            df.rename(columns={'调研次数': str(year_month)}, inplace=True)
            output_dict[year_month] = df

        # 将df进行拼接
        output_df = pd.DataFrame()
        for (k, v) in output_dict.items():
            # print(v)
            output_df = pd.concat([output_df, v])
            # output_df = pd.merge(output_df, v, on= '调研次数')

        # 将空值替换为0
        output_df = output_df.fillna(0)

        # 对各个月进行汇总
        output_df = output_df.groupby(['股票代码', '股票名称']).sum().reset_index()

        # print(output_df)

        # 增加汇总这列
        output_df['汇总'] = output_df.sum(axis=1)
        # output_df['汇总'] = output_df.count()

        # 增加调研月计数这列
        output_df['调研月计数'] = output_df[(output_df > 0) == True].count(axis='columns') - 3

        # 根据汇总这列进行倒序排序
        output_df.sort_values('汇总', ascending=False, inplace=True)
        print(output_df)
        # 输出到文件
        df = pd.DataFrame(output_df)
        filename = self.dirname_展现数据 + "结果数据" + str(from_year_month) + "-" + str(length) + pf.Execl
        df.to_excel(filename)


if __name__ == '__main__':
    a = 上市公司调研情况月度数据处理()
    a.数据汇总_步骤一()
    # b = [201801,201802,201803,201804,201805,201806,201807,201808,201809,201810,201811]
    # for c in b:
    # a.数据汇总_步骤二(c)
    #a.数据汇总_步骤二(201901)
    #a.数据汇总_步骤二(201902)
    #a.数据汇总_步骤二(201910)
    #a.数据汇总_步骤二(201812)
    # a.数据展示(201501,12)
