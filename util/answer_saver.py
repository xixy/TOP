# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import sys
sys.path.append('../configure/')
sys.path.append('../model/')
sys.path.append('../dao/')
from answer import answer
from answerDAO import answerDAO
import configure
from selection_question_extractor import selection_question_extractor
from filepath import getFullFilePath
from selection_question import selection_question
from selection_questionDAO import selection_questionDAO
import codecs


class answer_saver(object):
    """用来存储标准答案到数据库中"""
    @classmethod
    def indexAnswerForSingleSet(cls,filepath,setid):
        """
        将一套题的答案存入到数据库中
        Args:
            filepath:答案文件路径，需要读取，然后进行处理
            setid:标示那套题的答案，例如TPO1
        Return:
            None
        """

        #首选读取文件，然后获取到3+6=9个list
        index_material={}
        f=codecs.open(filepath,encoding='utf-8')
        answer_list=[]
        lines=f.readlines()
        for line in lines:
            if len(line)<2:
                continue#空行
            line.strip()#去掉换行
            answers=line.split(',')
            answer_list.append(answers)
            line=f.readline()


        count=0#计数，用于构造R1或者L2
        #首先处理Reading的答案
        for answers in answer_list[:3]:
            if len(answers)<13:
                print "阅读答案少于13:"+filepath+":"+str(len(answers))
            #如果是完整的14个题
            if len(answers)==14:
                for single_answer in answers:
                    single_answer=single_answer.strip()#去掉换行
                    count+=1
                    asw=answer(setid,configure.ReadingMark+str(count),single_answer,configure.answer_officialid)
                    answerDAO.index(asw,configure.answer_officialmode)
            #如果是不完整的13个体，那么第13个可能没有，这个其实需要商榷
            else:
                for single_answer in answers:
                    single_answer=single_answer.strip()#去掉换行
                    count+=1
                    asw=answer(setid,configure.ReadingMark+str(count),single_answer,configure.answer_officialid)
                    answerDAO.index(asw,configure.answer_officialmode)

        #然后处理Listening的答案
        count=0
        for answers in answer_list[3:]:
            if len(answers)<5:
                print "听力答案小于5:"+filepath+":"+str(len(answers))
            for single_answer in answers:
                single_answer=single_answer.strip()#去掉换行
                count+=1
                asw=answer(setid,configure.ListeningMark+str(count),single_answer,configure.answer_officialid)
                answerDAO.index(asw,configure.answer_officialmode)
        pass

    @classmethod
    def indexAnswerForMultiSet(cls,filepaths,setid):
        """
        将多套题的答案存入到数据库中
        Args:
            filepaths:一个list，存放答案文件路径，需要读取，然后进行处理
            setid:标示那套题的答案，例如TPO1
        Return:
            None
        """
        for filepath in filepaths:
            cls.indexAnswerForSingleSet(filepath,setid)

if __name__ == '__main__':
    filepath='/Users/apple/Code/TOP/resources/questions/20170603/answer'
    answer_saver.indexAnswerForSingleSet(filepath,"20170603")
