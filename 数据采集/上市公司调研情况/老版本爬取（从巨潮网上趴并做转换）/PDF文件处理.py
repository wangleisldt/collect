import os

from 函数目录.function import file_List_Func

from 函数目录.function import 获取文件名前缀与后缀

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser, PDFDocument

import re
import pandas as pd


def 根据文件名获取年份(filename):
    list = filename.split('_')
    year = list[2].split('-')[0]
    return year


def pdf文件处理(dirname,filename):
    try:
        year = 根据文件名获取年份(filename)
        文件带全路径 = dirname + filename
        有起始的字符串 = False
        有结束的字符串 = True
        sum = 0

        print(文件带全路径)

        fp = open(文件带全路径, 'rb')  # rb以二进制读模式打开本地pdf文件
        # request = Request(url=_path, headers={'User-Agent': random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
        # fp = urlopen(request) #打开在线PDF文档

        # 用文件对象来创建一个pdf文档分析器
        praser_pdf = PDFParser(fp)

        # 创建一个PDF文档
        doc = PDFDocument()

        # 连接分析器 与文档对象
        praser_pdf.set_document(doc)
        doc.set_parser(praser_pdf)

        # 提供初始化密码doc.initialize("123456")
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            pass
            # raise PDFTextExtractionNotAllowed
        else:
            # 创建PDf资源管理器 来管理共享资源
            rsrcmgr = PDFResourceManager()

            # 创建一个PDF参数分析器
            laparams = LAParams()

            # 创建聚合器
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # 创建一个PDF页面解释器对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # 循环遍历列表，每次处理一页的内容
            # doc.get_pages() 获取page列表
            for page in doc.get_pages():
                # 使用页面解释器来读取
                interpreter.process_page(page)

                # 使用聚合器获取内容
                layout = device.get_result()

                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                for out in layout:
                    # 判断是否含有get_text()方法，图片之类的就没有
                    # if hasattr(out,"get_text"):
                    if isinstance(out, LTTextBoxHorizontal):
                        results = out.get_text().strip()
                        if '现场参观' in results and 有结束的字符串:
                            # print("results: " + results)
                            有起始的字符串 = True
                        elif 有起始的字符串 and 有结束的字符串:
                            if year in results or str(int(year) - 1) in results or '公司会议室' in results or '接待人员' in results:
                                有结束的字符串 = False
                            else:
                                #print(results)
                                count = 对获得的结果进行处理(results)
                                sum = sum + count

        return sum
    except:
        print("文件处理出错！")
        return 0

def 打开目录读取文件(dirname):

    List = []

    fileList = file_List_Func(dirname)
    for filename in fileList:
        文件名前缀,文件名后缀 = 获取文件名前缀与后缀(filename)
        if 文件名后缀 == 'DOC':
            #DOC文件转DOCX(dirname,filename,文件名前缀)
            pass
        elif 文件名后缀 == 'PDF':
            #print(filename)
            sum = pdf文件处理(dirname, filename)
            print(filename,sum)

            List.append(整理需要的数据(filename,dirname+filename,sum))

    #根据list产生dataframe
    df = pd.DataFrame(List, columns=['股票代码', '时间','文件名称', '数量'])
    df.to_excel("c:\\机构调研数据.xlsx")
    print(df)

def 对获得的结果进行处理(line):
    count =0
    myResultList = [x for x in re.split(";|,|\||\t|、|；|：|：",line) if x ]
    for element in myResultList:
        if len(element.strip()) >=4:
            count=count+1
    return count

def 整理需要的数据(filename,全路径,sum):
    list = []
    stockid = 根据文件名获取股票代码(filename)
    yearMonth = 根据文件名获取年月(filename)
    list.append(stockid)
    list.append(yearMonth)
    list.append(filename)
    #list.append(全路径)
    list.append(sum)
    return list

def 根据文件名获取股票代码(filename):
    return filename.split('_')[0]

def 根据文件名获取年月(filename):
    day = filename.split('_')[2]
    year = day.split('-')[0]
    month = day.split('-')[1]
    return year+month

if __name__ == '__main__':
    打开目录读取文件('C:\\量化\\基本面数据\\投资者关系活动记录表\\原始数据\\2018\\')
