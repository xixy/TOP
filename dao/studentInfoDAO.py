# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
sys.path.append('../configure/')
import pymongo
from studentInfo import studentInfo
from bson import json_util as jsonb
from dbop import ip,port
import configure
class studentInfoDAO(object):
    """学生信息的持久化"""

    client=pymongo.MongoClient(ip,port)
    db=client.users#db
    collection=db.student#collection
    def __init__(self):
        pass

    @classmethod
    def index(cls,studentInfo):
    	"""保存学生信息到数据库中
        Args:
            studentInfo:学生信息
        Return:
            None
        """
        value={}
        value[configure.student_id]=studentInfo.id
    	value[configure.student_name]=studentInfo.username
    	value[configure.student_password]=studentInfo.password
        value[configure.student_questions]=studentInfo.questions
        cls.collection.insert(value)

    @classmethod
    def delete(cls,studentInfo):
    	"""删除学生信息"""
        value={}
        value[configure.student_id]=studentInfo.id
    	value[configure.student_name]=studentInfo.username
        cls.collection.find_one_and_delete(value)

    @classmethod
    def valid(cls,username,password):
    	"""验证学生登陆
        Args:
            username:学生用户名
            password:学生密码
        Return:
            如果验证成功，返回学生id
            否则返回-1
        """
        value={}
    	value[configure.student_name]=username
    	value[configure.student_password]=password
    	count = cls.collection.count(value)
    	if count==1:
    		for i in cls.collection.find(value):
    			return i[configure.student_id]
    	else:
    		return -1
    
    @classmethod
    def addQuestionSets(cls,id,question_set):
        """
        向学生增加可以做的题
        Args:
            id:学生id
            question_set:需要加入的题，一个list
        Return:
            成功，返回1
            失败，返回-1
        """

        #首先查看学生是否存在
        value={}
        value[configure.student_id]=id
        count=cls.collection.count(value)

        #如果找到
        if count==1:
            for result in cls.collection.find(value):
                result[configure.student_questions].extend(question_set)
                #按照时间排序
                result[configure.student_questions].sort()
                #然后进行更新
                cls.collection.update(value,result)
                return 1
        #如果没有找到学生
        else:
            return -1






if __name__=='__main__':
    studentInfo=studentInfo(2,"xixiangyu",123456)
    studentInfoDAO.index(studentInfo)

    studentInfoDAO.addQuestionSets(2,["TPO1","TPO2","TPO15","TPO16"])
    print studentInfoDAO.valid("xixiangyu",123456)
    # studentInfoDAO.delete(studentInfo)
