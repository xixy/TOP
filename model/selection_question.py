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
    def getSingleQuestion(cls,question,type):
        """用于将题库中读取的内容转化为Json格式，将来存入数据库中

        Args:
            question:一个list代表一道题
        Returns:
            返回dict，代表一道题，只有题干和选项，没有index
        """
        value={}
	#插入题干
	value[configure.selection_stem]=question[0]
        #插入选项
	value[configure.selection_options]={}
	length=len(question[1:])
	for k,v in zip(cls.index[:length],question[1:length]):
	    value[configure.selection_options][k]=v
        #插入是否为最后一题
        value[configure.isLast]=question[-1]
        #插入类型
        if len(value[configure.selection_options])==4:
            #如果是听力题，且题干中存在choose two answers,则是多选题
            if cmp(type,configure.Listening)==0:
                if cls.isMultipleSelectionQuestion(value):
                    value[configure.question_type]=configure.l_multiple_selection_type
                else:
                    value[configure.question_type]=configure.single_selection_type
            else:
                #普通选择题
                value[configure.question_type]=configure.single_selection_type

        else:
            #插入题，没有选项
            if len(value[configure.selection_options])==0:
                
                value[configure.question_type]=configure.insert_selection_type
            else:
                #多选题
                #如果是Reading的部分
                if cmp(type,configure.Reading)==0:
                    value[configure.question_type]=configure.r_multiple_selection_type
                #如果是Listening部分
                else:
                    if cmp(type,configure.Listening)==0:
                        value[configure.question_type]=configure.l_multiple_selection_type
        return value
    @classmethod
    def isMultipleSelectionQuestion(cls,value):
        """
        判断是否多选题
        """

        for twoSelectionMark in configure.ListeningTwoSelectionMark:
            if twoSelectionMark in value[configure.selection_stem]:
                return True
        for threeSelectionMark in configure.ListeningThreeSelectionMark:
            if threeSelectionMark in value[configure.selection_stem]:
                return True
        return False

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
	    result=cls.getSingleQuestion(question,type)
	    # print result
            result[configure.index]=configure.Mark[type]+str(i)
	    i+=1
	    results.append(result)
        return results

if __name__ == '__main__':
    questions=selection_question.test()
    # for question in questions:
    #     print question


