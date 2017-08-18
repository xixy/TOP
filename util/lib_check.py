# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../model/')
sys.path.append('../configure/')
sys.path.append('../dao/')

import pymongo
from answerDAO import answerDAO
from configure import ip,port
import configure
from selection_question import selection_question
from selection_questionDAO import selection_questionDAO
client=pymongo.MongoClient(ip,port)
#问题的数据库
db=client.questions
answer_db=client.answers
#答案的数据库
collectionlist=db.collection_names()
answer_collection_list=answer_db.collection_names()

def check():
    """
    对题目和答案都进行检查
    """
    check_questions()
    check_answers()

def check_questions():
    """
     对存储的问题进行检查
    """
    for collectionname in collectionlist:
        # print collectionname
        collection=db[collectionname]
        #查找Reading插入题的数量
        value={configure.question_type:configure.insert_selection_type}
        for question in collection.find(value):
            if "four squares" in question[configure.selection_stem]:
                continue
            print "阅读部分题干不存在插入题:"+collectionname
            print question

        #查找Reading多选题的数量
        value={configure.question_type:configure.r_multiple_selection_type}
        for question in collection.find(value):
            #判断是否有多选表示
            if selection_question.isMultipleSelectionQuestion(question):
                continue
            if "Prose" in question[configure.selection_stem] or "Answer" in question[configure.selection_stem] or "Drag" in question[configure.selection_stem]:
                continue
            print "阅读部分题干不存在多选题:"+collectionname
            print question

        #查找听力多选题
        value={configure.question_type:configure.l_multiple_selection_type}
        count=collection.find(value).count()
        for question in collection.find(value):
            if selection_question.isMultipleSelectionQuestion(question):
                continue
            #如果有问题
            print "听力部分题干不存在多选说明:"+collectionname
            print question

        #查看作文题
        #查找第一题
        value={configure.index:"W1"}
        if collection.find(value).count()==0:
            print "写作题第一题不存在："+collectionname
            continue
        question=collection.find_one(value)

        if configure.writing_stem not in question.keys() or question[configure.writing_stem]==[]:
            print "写作题第一题没有题干："+collectionname
        if configure.writing_article not in question.keys() or question[configure.writing_article]==[]:
            print "写作题第一题没有文章："+collectionname
        if configure.writing_record not in question.keys() or question[configure.writing_record]==[]:
            print "写作题第一题没有听力文本："+collectionname
        #查找第二题
        value={configure.index:"W2"}
        if collection.find(value).count()==0:
            print "写作题第二题不存在："+collectionname
            continue
        question=collection.find_one(value)
        if configure.writing_stem not in question.keys() or question[configure.writing_stem]==[]:
            print "写作题第二题没有题干："+collectionname

        #　检查口语题
        value={configure.index:"S1"}
        if collection.find(value).count()==0:
            print "听力题第1题不存在："+collectionname
            continue
        value={configure.index:"S2"}
        if collection.find(value).count()==0:
            print "听力题第2题不存在："+collectionname
            continue
        value={configure.index:"S3"}
        if collection.find(value).count()==0:
            print "听力题第3题不存在："+collectionname
            continue
        question=collection.find_one(value)
        if question[configure.listening_stem]=="":
            print "听力题第3题题干为空"+collectionname
            continue
        if question[configure.listening_article]=="":
            print "听力题第3题题干为空"+collectionname
            continue           
        if question[configure.listening_record]=="":
            print "听力题第3题题干为空"+collectionname
            continue   
        value={configure.index:"S4"}
        if collection.find(value).count()==0:
            print "听力题第4题不存在："+collectionname
            continue
        question=collection.find_one(value)
        if question[configure.listening_stem]=="":
            print "听力题第4题题干为空"+collectionname
            continue
        if question[configure.listening_article]=="":
            print "听力题第4题题干为空"+collectionname
            continue           
        if question[configure.listening_record]=="":
            print "听力题第4题题干为空"+collectionname
            continue
        value={configure.index:"S5"}
        if collection.find(value).count()==0:
            print "听力题第5题不存在："+collectionname
            continue
        question=collection.find_one(value)
        if question[configure.listening_stem]=="":
            print "听力题第5题题干为空"+collectionname
            continue

        if question[configure.listening_record]=="":
            print "听力题第5题题干为空"+collectionname
            continue   
        value={configure.index:"S6"}
        if collection.find(value).count()==0:
            print "听力题第6题不存在："+collectionname
            continue
        question=collection.find_one(value)
        if question[configure.listening_stem]=="":
            print "听力题第6题题干为空"+collectionname
            continue

        if question[configure.listening_record]=="":
            print "听力题第6题题干为空"+collectionname
            continue  
 
def check_answers():
    """
    对答案进行检查
    """
    #先检查是否所有的多选题答案都是多个
    for collectionname in collectionlist:
        collection=db[collectionname]
        #查找Reading多选题的数量
        value={configure.question_type:configure.r_multiple_selection_type}
        for question in collection.find(value):
            index=question[configure.index]
            #查找多选题答案
            answer=answerDAO.querySingleAnswer(configure.answer_officialid,collectionname[3:],index,configure.answer_officialmode)
            if len(answer)<2:
                print "多选题答案小于2:"+collectionname+":"+index
         #查找Reading拖拽题的数量
        value={configure.question_type:configure.drag_selection_type}
        for question in collection.find(value):
            index=question[configure.index]
            #查找多选题答案
            answer=answerDAO.querySingleAnswer(configure.answer_officialid,collectionname[3:],index,configure.answer_officialmode)
            if len(answer)<2:
                print "多选题答案小于2:"+collectionname+":"+index
        #查找Listening多选题的数量
        value={configure.question_type:configure.l_multiple_selection_type}
        for question in collection.find(value):
            index=question[configure.index]
            #查找多选题答案
            answer=answerDAO.querySingleAnswer(configure.answer_officialid,collectionname[3:],index,configure.answer_officialmode)
            if len(answer)<2:
                print "多选题答案小于2:"+collectionname+":"+index

    #检查答案是多个的对应的题目是否都是多选题
    for collectionname in answer_collection_list:
        if configure.answer_officialmode not in collectionname:
            continue
        collection=answer_db[collectionname]
        value={}
        answers=collection.find_one(value)
        for index in answers:
            #如果是听力题或者阅读题，并且是多选
            if index.startswith('R') or index.startswith('L'):

                if len(answers[index])>=2:
                    #判断题目是否多选
                    question=selection_questionDAO.getSelectionQuestion(collectionname[3:11],index)
                    question_type=question[configure.question_type]
                    if question_type == configure.r_multiple_selection_type or question_type== configure.l_multiple_selection_type or question_type==configure.drag_selection_type:
                        continue
                    else:
                        print "多个答案对应的题目不是多选题"+collectionname+":"+index+":"+answers[index]+":"+str(len(answers[index]))
                        print question





if __name__ == '__main__':
    check()
