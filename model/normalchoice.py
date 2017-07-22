# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import sys
sys.path.append('../util/')
from fileIO import fileIO,testpath
stem="stem"
options="options"
class normal_choice(object):
    """选择题，一般为4个选项，可能有6个选项"""
    index=["A","B","C","D","E","F","G","H","I","J","K"]

    @classmethod
    def getJsonFromList(cls,question):
        """用于将题库中读取的内容转化为Json格式，将来存入数据库中

        Args:
            question:一个list
        Returns:
            返回dict
        """
        value={}
	#插入题干
	value[stem]=question[0]
	value[options]={}
	length=len(question[1:])
	for k,v in zip(cls.index[:length],question[1:]):
	    value[options][k]=v
	return value


if __name__ == '__main__':
	questions=fileIO.getReadingQuestions(testpath)
	for question in questions:
		normal_choice.getJsonFromList(question)

