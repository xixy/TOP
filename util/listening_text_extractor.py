# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../configure/')
import codecs
import shutil
import re
import configure


class listening_text_extractor(object):
    """用于提取听力的文本"""
    def __init__(self):
        super(listening_text_extractor, self).__init__()

    @classmethod
    def getListeningText(cls,filepath):
        """
        读取文件，并且将听力文本返回
        Args:
            filepath:文件路径
        return
            返回一个dict
        """
        result={}
        f=codecs.open(filepath,encoding='utf-8')  
        index=filepath[-5:-4]
        result[configure.index]=configure.ListeningRecordMark+str(index)
        result[configure.listening_record]=[]
        lines=f.readlines()

        #获取全文
        for line in lines:
            result[configure.listening_record].append(line)

        return result

if __name__ == '__main__':
    testpath="/Users/apple/Code/TOP/resources/questions/20170603/Listening/Text/L1.txt"
    print listening_text_extractor.getListeningText(testpath)


