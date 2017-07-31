# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
sys.path.append('../configure/')
import pymongo
from bson import json_util as jsonb
from dbop import ip,port
import configure

class speaking_questionDAO(object):
    """用于口语题的持久化和查询"""
    def __init__(self):
        super(speaking_questionDAO, self).__init__()

    client=pymongo.MongoClient(ip,port)
    db=client.questions

    @classmethod
    def getCollectionName(cls,setid):
        """
        返回TPO20170603
        """
        return configure.question_prefix+str(setid)   

    @classmethod
    def indexQuestions(cls,setid,question):
        """
        将若干个选择题存入道题库中
        Args:
            setid:第几套题例如TPO1
            question:一个json，存放一道题，包括了index、stem、article、record
        """

        collection=cls.db[cls.getCollectionName(setid)]

        value={}
        value[configure.index]=question[configure.index]
        print value
        #去掉已有的该题
        # collection.remove(value)
        #插入
        # print question
        collection.insert(question)

    @classmethod
    def getSpeakingQuestion(cls,setid,index):
        """用于获取某套题的题干和选项
        Args:
            setid:第几套题例如TPO1
            index:第几题
        Return:
            一个dict
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


if __name__ == '__main__':
    print speaking_questionDAO.getSpeakingQuestion("20170603","S1")





