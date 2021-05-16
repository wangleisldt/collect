from 数据采集.机构持股.机构持股采集 import 从文件获取机构持股数据
from 函数目录.date import get_1_quarter_before
from 数据采集.股票清单.股票清单获取 import StockDict

# 数据类型
#            日期  机构属性  持股家数(家)         持股总数          持股市值  占总股本比例(%)  占流通股比例(%)
# 0  2020-03-31    基金      202    474005841  6.067275e+09   2.442584   2.442604
# 1  2020-03-31  QFII        0            0  0.000000e+00   0.000000   0.000000
# 2  2020-03-31    社保        1     95029523  1.216378e+09   0.489694   0.489697
# 3  2020-03-31    券商       26      3026878  3.944340e+07   0.015598   0.015598
# 4  2020-03-31    保险        3  11245119438  1.439375e+11  57.946856  57.947322
# 5  2020-03-31    信托        0            0  0.000000e+00   0.000000   0.000000
# 6  2020-03-31  机构汇总      232  11817181680  1.512606e+11  60.894731  60.895221

def 获取指定季度前几个月的数据(year,quarter ,num):
    output_dict = {}
    for i in range(0,num):
        dict = 从文件获取机构持股数据(year, quarter)
        # print(dict)
        key = f'{year}-{quarter}'
        output_dict[key]=dict
        year,quarter = get_1_quarter_before(year,quarter)
    return output_dict

def 获取机构持股指定数据(dict,stockid,year,quarter,type,col):
    try:
        key = f'{year}-{quarter}'
        df = dict[key][stockid]
        return df[df['机构属性']==type][col].values[0]
    except:
        return 0

if __name__ == '__main__':
    dict = 获取指定季度前几个月的数据(2020,1,1)

    print("start")
    for element in StockDict().stockIdList:
        # output = 获取机构持股指定数据(dict, element, 2020, 1, '机构汇总', '持股家数(家)')
        output = 获取机构持股指定数据(dict, element, 2020, 1, '机构汇总', '占总股本比例(%)')

        print(output)
    print("end")
