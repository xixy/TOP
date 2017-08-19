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


def getFullDirectoryPath(directory,result):
    """
    获取到directory下的所有Directory
    Args:
        directory:目标目录
        result:一个list，用来存放所有的文件夹
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

def getQuestionSetFilePath(directory,results):
    """
    获取到questinos下面的dict，其中key是题号，vlaue是所有的filepath，包括选择题、听力题、答案
    """
    for parent,dirnames,filenames in os.walk(directory):
        for dirname in dirnames:
            #只获取第一层目录
            if dirname.isdigit():
                result={}
                childDirectory=os.path.join(parent,dirname)
                filePathList=[]
                getFullFilePath(childDirectory,filePathList)
                result[dirname]=filePathList
                results.append(result)




if __name__=='__main__':
    rootdir='../resources/questions/'
    filePathList=[]
    getQuestionSetFilePath(rootdir,filePathList)
    for filePath in filePathList:
        print filePath
