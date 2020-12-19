from 函数目录.function import file_List_Func
from 函数目录 import profile as pf
from 函数目录.function import 获取文件名前缀与后缀

from 数据采集.上市公司调研情况.处理字符串获取机构名称 import 处理表格中的字符串

import os
import docx


def 处理某月所有DOCX文件(yearMonth):

    #产生需要打开的目录
    base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
    dirname = "%s%s%s%s%s%s%s%s" % (
    base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR, yearMonth[0:4], pf.SEPARATOR)

    #打开根据年月打开目录读取里面的文件
    fileList = file_List_Func(dirname)
    for filename in fileList:
        文件名前缀, 文件名后缀 = 获取文件名前缀与后缀(filename)
        if 文件名后缀 == 'DOCX' and 文件名前缀.split('_')[2].split('-')[1] == yearMonth[4:6]:
            #print(filename)
            sum = 处理某个DOCX文件(dirname, filename)
            print(filename,sum)
        elif 文件名后缀 == 'PDF':
            # print(filename)
            pass

def 处理某个DOCX文件(dirname,filename):
    def 打印输出(listReturn,filename,是否打印输出=False):
        if 是否打印输出:
            for element in listReturn:
                print(element, filename)

    sum = 0
    sumList = []
    开关 = False
    doc = docx.Document(os.path.join(dirname, filename))

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if '参与单位' in row.cells[0].text or '主办单位' in row.cells[0].text or '来访单位' in row.cells[0].text or '参加单位' in row.cells[0].text or \
                        '参加人员' in row.cells[0].text or '参与人员' in row.cells[0].text or '及人员姓名' in row.cells[0].text:
                    if table._column_count == 1:
                        开关 = True
                    else:
                        if cell.text != row.cells[0].text:
                            listReturn = 处理表格中的字符串(cell.text)
                            sumList = sumList + listReturn
                            打印输出(listReturn, filename)
                elif 开关 == True:
                    listReturn = 处理表格中的字符串(cell.text)
                    sumList = sumList + listReturn
                    打印输出(listReturn, filename)
                    开关 = False

    sum = len(list(set(sumList)))
    if sum is None:
        sum = 0
    return sum


if __name__ == '__main__':
    #打开目录读取文件('C:\\量化\\基本面数据\\投资者关系活动记录表\\原始数据\\2019\\')
    处理某月所有DOCX文件('201802')

