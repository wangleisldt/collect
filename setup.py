#!/usr/bin/python3
#-*- encoding: UTF-8 -*-
from setuptools import setup

setup(
    name = "proj-celery",          # 包名
    version = "0.1",              # 版本信息
    packages = ['proj'],  # 要打包的项目文件夹
    include_package_data=True,    # 自动打包文件夹内所有数据
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性
    author='Hui',
    install_requires = [          # 安装依赖的其他包
    #'celery',
    ],


    # 如果要上传到PyPI，则添加以下信息
    # author = "Me",
    # author_email = "me@example.com",
    # description = "This is an Example Package",
    # license = "MIT",
    # keywords = "hello world example examples",
    # url = "http://example.com/HelloWorld/

 )
