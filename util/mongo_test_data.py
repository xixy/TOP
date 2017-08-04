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

questionDirectory='../resources/questions'

if __name__ == '__main__':
    #生成题和答案
    results=[]
    #获取所有题的路径和名称
    getQuestionSetFilePath(questionDirectory,results)
    print "共发现%d套题" % len(results)
    for result in results:
        for setid in result.keys():
            print "发现题库："+setid
            question_saver.savequestions(setid,result[setid])
    #生成管理员
    admin1=admin(1,"xxy","123456")
    adminDAO.delete(admin1)
    adminDAO.index(admin1)
    #生成学生
    student1=studentInfo(1,"xxy","123456")
    studentInfoDAO.delete(student1)
    studentInfoDAO.index(student1)

    #给学生插入题
    studentInfoDAO.addQuestionSetsForStudent(1,["20170603","20170325","20170415"])

    #给学生提交几个答案
    asw=answer("20170603","R3","A", 1)
    answerDAO.index(asw,configure.answer_practicemode)
    asw=answer("20170603","L1","C",1)
    answerDAO.index(asw,configure.answer_practicemode)
    asw=answer("20170603","R3","D",1)
    answerDAO.index(asw,configure.answer_exammode)
    print "数据导入完毕"
