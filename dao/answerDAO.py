#! /usr/local/bin/python

import sys
sys.path.append('../model/')
import pymongo
from answer import answer
from bson import json_util as jsonb
from dbop import ip,port

class answerDAO(object):
    """docstring for answerDAO"""
    client=pymongo.MongoClient(ip,port)
    db=client.answers
    def __init__(self):
        super(answerDAO, self).__init__()

    @classmethod
    def index(cls,answer):
        value={}
        value["setid"]=answer.setid
    	value["userid"]=answer.userid
        collection=cls.db[answer.setid]
        count=collection.count(value)
        if count==0:
            print 0
            value[answer.index]=answer.choice
            collection.insert(value)
        else:
            print 1
            newchoice={}
            newchoice["setid"]=answer.setid
            newchoice["userid"]=answer.userid
            newchoice[answer.index]=answer.choice
            collection.update(value,newchoice)
        for data in collection.find():
        	print data
    @classmethod
    def clearAllAnswers(cls,userid):
        value={}
        value["userid"]=userid
        collectionlist=cls.db.collection_names()
        for collection in collectionlist:
            cls.db[collection].remove(value)

    @classmethod
    def querySingleAnswer(cls,userid,setid,index):
        value={}
        value["userid"]=userid
        collection=cls.db[setid]
        count=collection.count(value)
        if count==1:
            for i in collection.find(value):
                print "We find it"
                return i[index]
        else:
            return -1


        collectionlist=cls.db.collection_names()
        for collection in collectionlist:
            cls.db[collection].remove(value)
if __name__=='__main__':
    asw=answer("TPO1","R3","A",1)
    answerDAO.index(asw)
    print answerDAO.querySingleAnswer(1,"TPO1","R3")
    answerDAO.clearAllAnswers(1)