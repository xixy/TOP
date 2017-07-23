# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import sys
sys.path.append('../util/')
sys.path.append('../configure/')
from selection_question_extractor import selection_question_extractor,testpath
import configure

class selection_question(object):
    """选择题，一般为4个选项，可能有6个选项"""
    index=["A","B","C","D","E","F","G","H","I","J","K"]

    @classmethod
    def getSingleQuestion(cls,question):
        """用于将题库中读取的内容转化为Json格式，将来存入数据库中

        Args:
            question:一个list代表一道题
        Returns:
            返回dict，代表一道题，只有题干和选项，没有index
        """
        value={}
	#插入题干
	value[configure.selection_stem]=question[0]
	value[configure.selection_options]={}
	length=len(question[1:])
	for k,v in zip(cls.index[:length],question[1:]):
	    value[configure.selection_options][k]=v
        return value

    @classmethod
    def test(cls):
    	questions=selection_question_extractor.test()
	results=cls.getSetQuestion(questions,configure.Reading)
	return results

    @classmethod
    def getSetQuestion(cls,questions,type):
	"""
	将多个题转化为Json格式
	 Args:
	    questinos:一个list，元素也是list，一个元素代表一个题
	 Return:
	    返回一个list，元素是dict，表示一道题，包括题干、选项和index
	"""
	i=1#用来表示index
	results=[]
        for question in questions:
	    result=cls.getSingleQuestion(question)
	    result[configure.index]=configure.Mark[type]+str(i)
	    i+=1
	    results.append(result)
        return results

if __name__ == '__main__':
    questions=selection_question.test()
    for question in questions:
        print question


