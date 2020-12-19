import os
from win32com import client as wc
from 函数目录.function import file_List_Func
from 函数目录.date import getYearMonthFromMonthLength
from 函数目录 import profile as pf

def 打开目录将doc文件转换为docx(dirname):
    fileList = file_List_Func(dirname)
    for filename in fileList:
        文件名前缀,文件名后缀 = 获取文件名前缀与后缀(filename)
        if 文件名后缀 == 'DOC':
            DOC文件转DOCX(dirname,filename,文件名前缀)


def 获取文件名前缀与后缀(filename):
    list = filename.split('.')
    return list[0],list[1]

def DOC文件转DOCX(dirname,filename,文件名前缀):
    try:
        print(filename)
        word = wc.Dispatch('Word.Application')
        doc = word.Documents.Open(os.path.join(dirname, filename))
        输出文件名 = "%s.DOCX" % (文件名前缀)
        doc.SaveAs(os.path.join(dirname, 输出文件名), 12, False, "", True, "", False, False, False, False)
        doc.Close()
        word.Quit()
        要删除的文件带全路径 = "%s%s" % (dirname,filename)
        print(要删除的文件带全路径)
        os.remove(要删除的文件带全路径)
        #return os.path.join(path, 'tmp.docx')  3296  2018年的文件数量
    except:
        print('文件处理出错！')

def 打开目录将doc文件转换为docx接口(startDate,monthLength):
    def 产生需要处理的yearMonthList(startDate,monthLength):
        yearMonthList = []
        for i in range( 0 ,int(monthLength)):
            yearMonth = getYearMonthFromMonthLength(startDate, i)
            #print(yearMonth)
            yearMonthList.append(yearMonth)

        return yearMonthList

    for element in 产生需要处理的yearMonthList(startDate,monthLength):

        year = ''
        if element[0:4] != year:
            base_dir_name = "%s%s%s" % (pf.GLOBAL_PATH, pf.SEPARATOR, pf.FUNDAMENTAL_DATA)
            dir_name = "%s%s%s%s%s%s%s%s" % (
                base_dir_name, pf.SEPARATOR, pf.投资者关系活动记录表, pf.SEPARATOR, pf.原始数据, pf.SEPARATOR, element[0:4] , pf.SEPARATOR)
            打开目录将doc文件转换为docx(dir_name)
            year = element[0:4]
        else:
            pass

if __name__ == '__main__':
    打开目录将doc文件转换为docx接口('201801', 12)

