# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
sys.path.append('../configure/')
import pymongo
from selection_question import selection_question
from bson import json_util as jsonb
from dbop import ip,port
import configure

class selection_questionDAO(object):
    """获取题库的选择题"""
    client=pymongo.MongoClient(ip,port)
    db=client.questions

    @classmethod
    def getCollectionName(cls,setid):
        """
        返回TPO20170603
        """
        return configure.question_prefix+str(setid)


    @classmethod
    def getSelectionQuestion(cls,setid,index):
        """用于获取某套题的题干和选项
        Args:
            setid:第几套题例如TPO1
            index:第几题
        Return:
            一个dict，例如{"index":"R1","stem":"The word "occasionally" in the passage is closest in meaning to",
            options:{"A":"hello","B":"hi","C":"world","D":"nice"}}
        """
        value={}
        value[configure.index]=index
        collection=cls.db[cls.getCollectionName(setid)]
        count=collection.count(value)
        result={}
        #如果找到
        if count==1:
            for result in collection.find(value):
                result.pop("_id")
                return result
        #如果没找到
        else:
            return configure.FAIL_CODE

    @classmethod
    def indexQuestions(cls,setid,questions):
        """
        将若干个选择题存入道题库中
        Args:
            setid:第几套题例如TPO1
            questions:一个list，元素是json，存放每一道题
        """

        #如果已经存过了，就先删除现在的题库

        collection=cls.db[cls.getCollectionName(setid)]
        value={}
        for question in questions:
            value[configure.index]=question[configure.index]
            collection.remove(value)
            collection.insert(question)



    @classmethod
    def test(cls):
        questions=selection_question.test()
        cls.indexQuestions("TPO1",questions)



if __name__ == '__main__':
    selection_questionDAO.test()
    # print selection_questionDAO.getSelectionQuestion("TPO1","R14")
