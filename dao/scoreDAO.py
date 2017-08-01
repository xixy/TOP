# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
sys.path.append('../configure/')
import pymongo

from score import score
from bson import json_util as jsonb
from configure import ip,port
from answermode import exammode,practicemode,officialmode,officialid
from answerDAO import answerDAO

class scoreDAO(object):
    """用来计算评分
    需要对听力和阅读两个部分都进行评分
    """

    client=pymongo.MongoClient(ip,port)
    db=client.answers

    def getScore(score):
    	"""
		用来计算学生的评分
		Args:
			score:需要选择的模型
		Return:
			返回得分
		"""
		student_answers=answerDAO.queryAnswerForTPOSet()
		value={}
    	value["userid"]=score.userid
        collection=cls.db[score.setid+score.mode]
        count=collection.count(value)
        student_answers={}
        official_answers={}
        point=0

        #如果找到
        if count==1:
        	for i in collection.find(value):
        		student_answers=i
        		break

        else:
        	return 0

        #获取标准答案

        #如果找到
        if count==1:
        	for i in collection.find():
        		official_answers=i
        		break
        #如果没有找到
        else:
        	return 0

        #进行比较
        for k in student_answers:
        	if official_answers.has_key(k):
        		#如果相等，就去计算分值
        		if(cmp(official_answers[k],student_answers[k])==0):
        			point+=1

        		pass





		pass
		
