# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import os
import os.path



def getFullFilePath(directory,result):
    """
    获取到directory下的所有文件
    Args:
        directory:目标目录
        result:一个list，用来存放所有的文件
    """
    for parent,dirnames,filenames in os.walk(directory):
        for filename in filenames:
            filepath=os.path.join(parent,filename)
            if filepath in result:
                continue
            result.append(filepath)
        for dirname in dirnames:
            childDirectory=os.path.join(parent,dirname)
            getFullFilePath(childDirectory,result)
            pass


if __name__=='__main__':
    rootdir='../resources/questions/TPO1'
    filePathList=[]
    getFullFilePath(rootdir,filePathList)
    for filePath in filePathList:
        print filePath
