# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
sys.path.append('../configure/')
import pymongo
from answer import answer
from bson import json_util as jsonb
from dbop import ip,port
import configure

class answerDAO(object):
    """答案的持久化"""
    client=pymongo.MongoClient(ip,port)
    db=client.answers
    def __init__(self):
        super(answerDAO, self).__init__()

    @classmethod
    def getCollectionName(cls,setid,mode):
        """
        根据题目和mode来获取相应的数据库
        Args:
            setid:第几套题例如TPO1
            mode:需要查找什么模式下的答案，例如configure
        """
        return configure.answer_prefix+setid+mode

    @classmethod
    def index(cls,answer,mode):
        """用于将答案存入，如果答案已经存在，就进行更新
        如果答案不存在，就直接去

        Args:
            answer: 答案模型的实例
            mode: 模式分为三种：PRACTICE、EXAM、OFFICIAL
            分别代表练习、考试和标准答案
        Returns:
            返回nothing
        """
        value={}
    	value[configure.answer_userid]=answer.userid
        collection=cls.db[cls.getCollectionName(answer.setid,mode)]
        count=collection.count(value)
        # 没有打过题
        if count==0:
            value[answer.index]=answer.choice
            collection.insert(value)
        # 如果已经答过题了
        else:
            for i in collection.find(value):
                i[answer.index]=answer.choice
                collection.update(value,i)


    @classmethod
    def clearAllAnswers(cls,userid):
        """用于清除特定用户的所有答案
        暂时将练习答案和考试答案都清除

        Args:
            userid:用户id
        Returns:
            返回nothing
        """
        value={}
        value[configure.answer_userid]=str(userid)
        collectionlist=cls.db.collection_names()
        for collection in collectionlist:
            cls.db[collection].remove(value)


    @classmethod
    def querySingleAnswer(cls,userid,setid,index,mode):
        """用于获取用户的某个答案
        Args:
            userid:用户id
            setid:第几套题例如TPO1
            index:题号，例如R1，L2
            mode:需要查找什么模式下的答案，例如configure.answer_practicemode或者configure.answer_exammode

        """
        value={}
        value[configure.answer_userid]=str(userid)
        collection=cls.db[cls.getCollectionName(setid,mode)]
        print value
        print cls.getCollectionName(setid,mode)
        count=collection.count(value)
        if count==1:
            for i in collection.find(value):
                if(i.has_key(index)):
                    print "We find it"
                    return i[index]
                else:
                    return configure.FAIL_CODE
        else:
            return configure.FAIL_CODE

    @classmethod
    def queryAnswerForTPOSet(cls,userid,setid,mode):
        """用于获取某套题的答案，包括Reading和Listening部分
        Args:
            userid:用户id 如果是官方答案，就是configure.FAIL_CODE
            setid:第几套题例如TPO1
            mode:什么模式，例如configure.answer_practicemode或者exammode，或者configure.answer_officialmode
        Return:
            一个dict
        """
        value={}
        value[configure.answer_userid]=str(userid)
        collection=cls.db[cls.getCollectionName(setid,mode)]
        count=collection.count(value)
        result={}
        #如果找到
        if count==1:
            for officlial_answer in collection.find(value):
                for item in officlial_answer:
                    if item.startswith('R') or item.startswith('L'):
                        result[item]=officlial_answer[item]
                return result
        else:
            return None



if __name__=='__main__':
    asw=answer("20170603","R3","A","1")
    answerDAO.index(asw,configure.answer_practicemode)
    asw=answer("20170603","L1","C","1")
    answerDAO.index(asw,configure.answer_practicemode)
    asw=answer("20170603","R3","D","1")
    answerDAO.index(asw,configure.answer_exammode)
    print answerDAO.querySingleAnswer(1,"20170603","R3",configure.answer_practicemode)
    print answerDAO.queryAnswerForTPOSet(1,"20170603",configure.answer_practicemode)
    # answerDAO.clearAllAnswers(1)