# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import sys
sys.path.append('../configure/')
import codecs
import shutil
import re
import configure

testpath="/Users/apple/Code/TOP/resources/questions/20150613/Reading/R1.txt"

class selection_question_extractor(object):

    option_pattern=re.compile(r'[A-F]+\)') #匹配选项的正则pattern
    option_pattern2=re.compile(r'[A-F]+\.') #匹配选项的正则pattern
    stem_pattern=re.compile(r'[0-9]+\.') #匹配题干的正则pattern

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
        lines=f.readlines()
        single_question=[]
        stem="" #题干部分

        for line in lines:
            if len(line)<3:
                continue
            # print line

            line=line.strip()#去掉\n
            # print line
            match=cls.stem_pattern.search(line)
            match1=cls.option_pattern.search(line)
            match2=cls.option_pattern2.search(line)

            #如果是选项部分
            if (match2 and line.startswith(match2.group())) or (match1 and line.startswith(match1.group())):
                # print line
                if len(stem)>0:
                    single_question.append(stem)
                stem=""
                single_question.append(line)
            else:
                #如果是新题的开始部分
                if match and line.index(match.group())<2:
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
                #如果不是选项部分，那么则是题干部分
                else:
                    #多余的题干就去掉
                    if stem=="":
                        continue
                    stem+=configure.LineBreakMark
                    stem+=line

        #加入最后一题
        #如果是个插入题
        if single_question==[]:
            single_question.append(stem)
            questions.append(single_question)
        #如果是个选择题，drag类题目
        else:
            single_question[0]=single_question[0][:3]+"Prose Summary<br>"+single_question[0][3:]
            questions.append(single_question)

        #首先加入是否为最后一题的标记
        for single_question in questions[:-1]:
            single_question.append(-1)
        questions[-1].append(1)

        return questions

    @classmethod
    def test(cls):
        results=cls.getSelectionQuestions(testpath)
        # for result in results:
        #     print result
        return results

if __name__ == '__main__':
    
    selection_question_extractor.test()
