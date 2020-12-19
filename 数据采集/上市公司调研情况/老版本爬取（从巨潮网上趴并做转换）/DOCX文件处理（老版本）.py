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
            处理某个DOCX文件(dirname, filename)
        elif 文件名后缀 == 'PDF':
            # print(filename)
            pass

def 处理某个DOCX文件(dirname,filename):
    sum = 0
    doc = docx.Document(os.path.join(dirname, filename))

    i = 0
    j = 0

    tables = [table for table in doc.tables];
    i = 0
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                if i ==1:
                    print(cell.text)
                    list = 处理表格中的字符串(cell.text)
                    for element in list:
                        print(element,filename)
                    sum = len(list) + sum
                elif i >= 2 and i <=3 :
                    if sum == 0:
                        print(len(cell.text))
                        print(cell.text)
                        list = 处理表格中的字符串(cell.text)
                        for element in list:
                            print(element, filename)
                        sum = len(list) + sum
                        print(filename,'#########################')
                else:
                    print(cell.text)

            i = i+1
    #print(sum)

    if sum ==0:
        print(filename)

    '''
    ii = 0
    if sum == 0:
        for table in tables:
            for row in table.rows:
                print(ii)
                for cell in row.cells:
                    print(cell.text)
                    print('###############################')
                ii = ii + 1

    ii = 0
    for table in tables:
        for row in table.rows:
            print(ii)
            for cell in row.cells:
                print(cell.text)
                print('#################################################\n')
            ii = ii + 1


'''





if __name__ == '__main__':
    #打开目录读取文件('C:\\量化\\基本面数据\\投资者关系活动记录表\\原始数据\\2019\\')
    处理某月所有DOCX文件('202011')
