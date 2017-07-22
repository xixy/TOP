# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
import pymongo
from normalchoice import normal_choice,item,options
from bson import json_util as jsonb
from dbop import ip,port
from answermode import exammode,practicemode,officialmode,officialid

class normalchoiceDAO(object):
	"""获取题库的选择题"""
	client=pymongo.MongoClient(ip,port)
    db=client.questions


    @classmethod
    def getChoice(cls,setid,index):
        """用于获取某套题的题干和选项
        Args:
            setid:第几套题例如TPO1
            index:第几题
        Return:
            一个dict，例如{"index":"R1","stem":"The word “occasionally” in the passage is closest in meaning to",
            options:{"A":"hello","B":"hi","C":"world","D":"nice"}}
        """
        value={}
        value["index"]=index
        collection=cls.db[setid]
        count=collection.count(value)
        result={}
        #如果找到
        if count==1:
            for questinos in collection.find(value):
            	result[item]=questinos[item]
            	result[options]=questinos[options]
                return result
        #如果没找到
        else:
            return None