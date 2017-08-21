# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import sys
sys.path.append('../configure/')
import codecs
import shutil
import re
import configure

class speaking_question_extractor(object):
    """
    读取文件，并将题目提取出来
    """
    def __init__(self):
        super(speaking_question_extractor, self).__init__()

    @classmethod
    def getSpeakingQuestion(cls,filepath):
        """
        读取文件，并且将题目提取出来，返回一个dict，包括index、stem、article、record
        Args:
            filepath:文件路径
        return
            返回一个dict
        """
        result={}
        f=codecs.open(filepath,encoding='utf-8')
        line=1
        stem=[]
        article=[]
        record=[]
        index=filepath[-6:-4]
        result[configure.index]=index
        if "S1" in filepath or "S2" in filepath:
            lines=f.readlines()
            for line in lines:
                if len(line)<3:
                    continue
                line=line.strip()

                stem.append(line)
            #完毕进行处理
            result[configure.listening_stem]=stem
            return result

        mode=0
        if "S3" in filepath or "S4" in filepath or "S5" in filepath or "S6" in filepath:
            lines=f.readlines()
            for line in lines:
                if len(line)<3:
                    continue
                line=line.strip()

                if "#article" in line:
                    mode=1
                    continue
                if "#record" in line:
                    mode=2
                    continue
                if "#question" in  line:
                    mode=3
                    continue
                    
                if mode==1:
                    article.append(line)
                if mode==2:
                    record.append(line)
                if mode==3:
                    stem.append(line)

            #完毕进行处理
            result[configure.listening_stem]=stem
            result[configure.listening_record]=record
            if article!=[]:
                result[configure.listening_article]=article
            return result

if __name__ == '__main__':
    filepath="/Users/apple/Code/TOP/resources/questions/20170603/Speaking/S5.txt"
    result=speaking_question_extractor.getSpeakingQuestion(filepath)
    print result





