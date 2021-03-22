import os
import pickle
import pathlib

from 函数目录 import profile as pf


#################################################
#   判断目录是否存在，如果不存在创建该目录
#################################################
def checkAndCreateDir(dirName):
    if os.path.exists(dirName):
        pass
    else:
        os.makedirs(dirName)
        print("\n创建目录：", dirName)


#################################################
#   从pkl文件读取数据到字典dict
#################################################
def getPklDataToDict(filename):
    pklFile = open(filename, 'rb')
    returnDict = pickle.load(pklFile)
    pklFile.close()
    return returnDict


#################################################
#   检测文件是否存在
#################################################
def check_file_exist(dirname, filename):
    checkAndCreateDir(dirname)
    path = pathlib.Path("%s%s%s" % (dirname, pf.SEPARATOR, filename))
    return path.is_file()


#################################################
#   保存文件
#################################################
def save_file_dataframe_to_execl(dirname, filename, df):
    if check_file_exist(dirname, filename):
        print("文件存在！")
    else:
        full_filename = dirname + pf.SEPARATOR + filename
        print(full_filename)
        df.to_excel(full_filename)
        print("%s  保存文件成功。" % (full_filename))


#################################################
#   扫描目录，返回文件名称List
#################################################
def file_List_Func(Path):
    fileList = []
    for file in os.listdir(Path):
        file_path = os.path.join(Path, file)
        if os.path.isdir(file_path):
            pass
        else:
            fileList.append(file)
    return fileList


#################################################
#   根据文件名称，分别获取 股票代码，年份，季度   文件每次例如 603985-2017-3.xlsx
#################################################
def from_filename_get_info(filename):
    return filename.split('.')[0].split('-')


#################################################
#   根据文件名称获取前缀与后缀
#################################################
def 获取文件名前缀与后缀(filename):
    list = filename.split('.')
    return list[0], list[1]


#################################################
#   将obj保存为pkl文件
#################################################
def save_pkl_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


#################################################
#   将读取pkl文件
#################################################
def load_pkl_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)
