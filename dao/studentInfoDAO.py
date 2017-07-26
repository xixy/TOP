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
        value[configure.student_classid]=studentInfo.classid
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
            否则返回configure.FAIL_CODE
        """
        value={}
    	value[configure.student_name]=username
    	value[configure.student_password]=password
    	count = cls.collection.count(value)
    	if count==1:
    		for i in cls.collection.find(value):
    			return i[configure.student_id]
    	else:
    		return configure.FAIL_CODE

    @classmethod
    def addQuestionSetsForStudent(cls,id,question_set):
        """
        向学生增加可以做的题
        Args:
            id:学生id
            question_set:需要加入的题，一个list
        Return:
            成功，返回1
            失败，返回configure.FAIL_CODE
        """

        #首先查看学生是否存在
        value={}
        value[configure.student_id]=int(id)
        count=cls.collection.count(value)

        #如果找到
        if count==1:
            incremental_question=[]
            for student in cls.collection.find(value):
                #如果题已经在了，就不能加入
                for question in question_set:
                    if question not in student[configure.student_questions]:
                        incremental_question.append(question)
                student[configure.student_questions].extend(incremental_question)
                #按照时间排序
                student[configure.student_questions].sort()
                #然后进行更新
                cls.collection.update(value,student)
                return 1
        #如果没有找到学生
        else:
            return configure.FAIL_CODE


    @classmethod
    def getAllStudents(cls):
        """
        获取所有的学生信息
        Return:
            一个列表，里面是所有的学生信息，每个元素是一个学生的信息
            [{u'username': u'xixiangyu', u'password': 123456, u'id': 1, u'questions': [u'TPO1', u'TPO15', u'TPO16', u'TPO2', u'TPO45']}, 
            {u'username': u'anxiao', u'password': 12345, u'id': 2, u'questions': []}]
        """
        students={}
        for student in cls.collection.find():
            student.pop('_id')
            students[student[configure.student_name]]=student

        return students

    @classmethod
    def getQuestionsOfSingleStudent(cls,id):
        """
        获取某个学生的买的所有题，返回的是题的setid，例如TPO1
        Args:
            id:学生id
        Return:
            一个存放题名称的list，例如["TPO1","TPO2"]
        """
        value={}
        value[configure.student_id]=int(id)
        count=cls.collection.count(value)

        #如果找到学生
        if count==1:
            for student in cls.collection.find(value):
                return student[configure.student_questions]
        #如果没找到
        else:
            return configure.FAIL_CODE







if __name__=='__main__':
    studentInfo=studentInfo(1,"anxiao","12345")
    studentInfoDAO.index(studentInfo)

    studentInfoDAO.addQuestionSetsForStudent(1,["20170603","20150703","20150809"])
    # print studentInfoDAO.valid("anxiao","12345")
    studentInfoDAO.getAllStudents()
    print studentInfoDAO.getQuestionsOfSingleStudent(1)
    # studentInfoDAO.delete(studentInfo)
