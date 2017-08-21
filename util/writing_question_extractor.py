# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import sys
sys.path.append('../configure/')
import codecs
import shutil
import re
import configure

class writing_question_extractor(object):
    """
    读取文件，并将题目提取出来
    """
    def __init__(self):
        super(writing_question_extractor, self).__init__()

    @classmethod
    def getWritingQuestion(cls,filepath):
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
        
        #如果是第二题，则需要提取stem
        if "W2" in filepath:
            lines=f.readlines()
            for line in lines:
                if len(line)<3:
                    continue
                line=line.strip()
                stem.append(line)
            #完毕进行处理
            result[configure.writing_stem]=stem
            return result

        #如果是第一题，则需要提取article、record、stem
        mode=0
        if "W1" in filepath:
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
                if "#question" in  line or "#Question" in line:
                    mode=3
                    continue
                    
                if mode==1:
                    article.append(line)
                if mode==2:
                    record.append(line)
                if mode==3:
                    stem.append(line)

            #完毕进行处理
            if stem==[]:
                stem.append(configure.writing_default_stem)
            result[configure.writing_stem]=stem
            result[configure.writing_record]=record
            result[configure.writing_article]=article
            return result

if __name__ == '__main__':
    filepath="/Users/apple/Code/TOP/resources/questions/20150418/Writing/W1.txt"
    result=writing_question_extractor.getWritingQuestion(filepath)
    print result





