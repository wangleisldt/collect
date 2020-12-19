from 数据采集.上市公司调研情况.获取上市公司调研情况 import 获取上市公司调研情况接口
from 数据采集.上市公司调研情况.WORD类型转换doc_docx import 打开目录将doc文件转换为docx接口
from 数据采集.上市公司调研情况.DOCX与PDF文件合并处理_一个月数据_及写文件 import 处理某月所有DOCX与PDF文件接口
from 数据采集.上市公司调研情况.数据汇总 import 上市公司调研情况月度数据合并处理接口


def 数据采集及处理(yearMonth,monthLength):
    print("1、开始采集数据。\n")
    获取上市公司调研情况接口(yearMonth,monthLength)
    print("\n2、转换doc文件为docx文件。\n")
    打开目录将doc文件转换为docx接口(yearMonth,monthLength)
    print("\n3、分析处理每个docx和pdf文件。\n")
    处理某月所有DOCX与PDF文件接口(yearMonth,monthLength)
    print("\n4、对每个股票的记录进行合并。\n")
    上市公司调研情况月度数据合并处理接口(yearMonth,monthLength)

if __name__ == '__main__':

    #参数含义，起始年月，月的步长
    数据采集及处理('201808',1)

    #展现数据，到指定目录中去拿
    #数据展现接口('201806',1)
