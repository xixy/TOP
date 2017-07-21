# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
import pymongo
from answer import answer
from bson import json_util as jsonb
from dbop import ip,port

class answerDAO(object):
    """答案的持久化"""
    client=pymongo.MongoClient(ip,port)
    db=client.answers
    def __init__(self):
        super(answerDAO, self).__init__()

    @classmethod
    def index(cls,answer,mode):
        """用于将答案存入"""
        value={}
    	value["userid"]=answer.userid
        collection=cls.db[answer.setid+"_"+mode]
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
        """用于清除用户的所有答案"""
        value={}
        value["userid"]=userid
        collectionlist=cls.db.collection_names()
        for collection in collectionlist:
            cls.db[collection].remove(value)


    @classmethod
    def querySingleAnswer(cls,userid,setid,index,mode):
        """用于获取用户的某个答案"""
        value={}
        value["userid"]=userid
        collection=cls.db[setid+"_"+mode]
        count=collection.count(value)
        if count==1:
            for i in collection.find(value):
                if(i.has_key(index)):
                    print "We find it"
                    return i[index]
                else:
                    return -1
        else:
            return -1

if __name__=='__main__':
    asw=answer("TPO1","R3","A",1)
    answerDAO.index(asw,"practice")
    asw=answer("TPO1","L1","C",1)
    answerDAO.index(asw,"practice")
    asw=answer("TPO2","R3","D",1)
    answerDAO.index(asw,"practice")
    print answerDAO.querySingleAnswer(1,"TPO1","R3","practice")
    # answerDAO.clearAllAnswers(1)