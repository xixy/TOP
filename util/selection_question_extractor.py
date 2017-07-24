# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import sys
sys.path.append('../configure/')
import codecs
import shutil
import re
import configure

testpath="/Users/apple/Code/TPO/resources/questions/TPO1/Reading/R1.txt"

class selection_question_extractor(object):
    """
    读取文件，并且将选择题提取出来
    """
    option_pattern=re.compile(r'[A-F]+\) ') #匹配选项的正则pattern
    stem_pattern=re.compile(r'[0-9]+\. ') #匹配题干的正则pattern

    """处理文件的读取"""
    def __init__(self):
        super(fileIO, self).__init__()
	
    @classmethod
    def getSelectionQuestions(cls,filepath):
        """
	读取文件，然后把题干和选项都放在了list中，一个list的元素是题干+选项，因为默认了题目之间有空格隔开，用来处理阅读和听力部分

	Args:
            filepath:文件路径

	Return
	    返回一个list，list中的内容是list，list中存放题干和选项，其中第十三题选项为空，只有题干
	"""
	f=codecs.open(filepath,encoding='utf-8')
	questions=[]
        line=1
	single_question=[]
	stem="" #题干部分
	while line:
            try:
	        line=f.readline()
		if len(line)<2:
		    continue
                line=line.strip()#去掉\n
		match=cls.stem_pattern.search(line)
	        #如果匹配到，意味着新题的开始
		if match:
		#如果是刚开始
		    if len(single_question)==0 and len(stem)==0:
			stem+=line
		    #如果前面已经有了题
		    else:
		        #如果是第13题出现，只有题干没有选项
			if len(stem)>0:
			    single_question.append(stem)
			questions.append(single_question)
			single_question=[]
			stem=line

		#如果没有匹配到
		else:
		    match=cls.option_pattern.search(line)
		    #如果匹配到是选项部分，那么直接加入
		    if match:
			if len(stem)>0:
			    single_question.append(stem)
			stem=""
			single_question.append(line)
		    #如果不是选项部分，那么则是题干部分
		    else:
                        stem+=configure.LineBreakMark
                        stem+=line
	    except UnicodeDecodeError,e:
		return None
	#加入最后一题
        questions.append(single_question)

        #首先加入是否为最后一题的标记
        for single_question in questions[:-1]:
            single_question.append(-1)
        questions[-1].append(1)

	return questions

    @classmethod
    def test(cls):
        results=cls.getSelectionQuestions(testpath)
        for result in results:
            print result
        return results

if __name__ == '__main__':
    selection_question_extractor.test()
