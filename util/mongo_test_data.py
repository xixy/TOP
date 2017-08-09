# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../configure/')
sys.path.append('../model/')
sys.path.append('../dao/')
from answer import answer
from answerDAO import answerDAO
import configure
from question_saver import question_saver
from admin import admin
from adminDAO import adminDAO
from studentInfo import studentInfo
from studentInfoDAO import studentInfoDAO
from filepath import getQuestionSetFilePath
from lib_check import check
import pymongo
from configure import ip,port
questionDirectory='../resources/questions'

client=pymongo.MongoClient(ip,port)
userdb=client.users#userdb
answerdb=client.answers
questiondb=client.questions


if __name__ == '__main__':
    #删除官方答案库
    collectionlist=answerdb.collection_names()
    for collectionname in collectionlist:
        if "official" in collectionname:
            collection=answerdb[collectionname]
            collection.remove({})
    #删除问题库
    collectionlist=questiondb.collection_names()
    for collectionname in collectionlist:
        collection=questiondb[collectionname]
        collection.remove({})
    
    #生成题和答案
    results=[]
    #获取所有题的路径和名称
    getQuestionSetFilePath(questionDirectory,results)
    print "共发现%d套题" % len(results)
    for result in results:
        for setid in result.keys():
            print "发现题库："+setid
            question_saver.savequestions(setid,result[setid])
    #进行测试
    check()
    #生成管理员
    userdb.admin.remove({})
    admin1=admin(1,"xxy","123456")
    adminDAO.delete(admin1)
    adminDAO.index(admin1)
    #生成学生
    userdb.student.remove({})
    student1=studentInfo("xxy","123456")
    studentInfoDAO.delete(1)
    studentInfoDAO.index(student1)

    #给学生插入题
    studentInfoDAO.addQuestionSetsForStudent(1,["20170603","20170325","20170415"])

    #给学生提交几个答案
    # asw=answer("20170603","R3","A", 1)
    # answerDAO.index(asw,configure.answer_practicemode)
    # asw=answer("20170603","L1","C",1)
    # answerDAO.index(asw,configure.answer_practicemode)
    # asw=answer("20170603","R3","D",1)
    # answerDAO.index(asw,configure.answer_exammode)
    print "数据导入完毕"
