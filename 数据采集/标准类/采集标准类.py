import requests
import json

import chardet

import pandas as pd

import time

import pickle

import os

from 函数目录 import profile as pf

from 函数目录.function import checkAndCreateDir, check_file_exist
from 数据采集.股票清单.股票清单获取 import StockDict
from 函数目录.date import getCurrentDate

def 请求数据(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    fencoding = chardet.detect(response.content)
    content = response.content.decode(fencoding['encoding'], errors='ignore')[13:]
    #print(content)
    return content



if __name__ == '__main__':
    pass

    #print(dict)