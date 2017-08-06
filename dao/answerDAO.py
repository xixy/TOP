# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
sys.path.append('../configure/')
sys.path.append('../util/')
import pymongo
from answer import answer
from bson import json_util as jsonb
from configure import ip,port
from studentInfoDAO import studentInfoDAO
from selection_questionDAO import selection_questionDAO
import configure
from dict_op import sortDict

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
        if not mode.startswith("_"):
            mode="_"+mode
        return configure.answer_prefix+str(setid)+mode

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
    	value[configure.answer_userid]=int(answer.userid)
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
        value[configure.answer_userid]=int(userid)
        collectionlist=cls.db.collection_names()
        for collection in collectionlist:
            cls.db[collection].remove(value)


    @classmethod
    def clearAnswersForQuestionSet(cls,userid,setid,mode,part):
        """用于清除特定用户的某套题的答案
        暂时将练习答案和考试答案都清除

        Args:
            userid:用户id
            setid:第几套题例如TPO1
            mode:什么模式，例如configure
            part:哪个部分？例如all、Listening、Reading、Speaking、Writing

        Returns:
            返回nothing
        """
        value={}
        value[configure.answer_userid]=int(userid)
        collection=cls.db[cls.getCollectionName(setid,mode)]
        #如果要删除所有的
        if part=="all":
            collection.remove(value)
        else:
            index=configure.Mark[part]
            newAnswers={}
            for answers in collection.find(value):

                #将答案进行便利，删掉其中包含index的部分
                for (k,v) in answers.items():
                    #如果key包含indexmark，就要删除
                    if index in k:
                        answers.pop(k)
                collection.update(value,answers)



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
        value[configure.answer_userid]=int(userid)
        collection=cls.db[cls.getCollectionName(setid,mode)]
        count=collection.count(value)
        if count==1:
            for i in collection.find(value):
                if(i.has_key(index)):
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
            一个dict,key是L1、L2、R1，value是C、D、BC选项
        """
        value={}
        value[configure.answer_userid]=int(userid)
        collection=cls.db[cls.getCollectionName(setid,mode)]
        count=collection.count(value)
        result={}
        #如果找到
        if count==1:
            #按照标准答案中给出的来进行
            answers=collection.find_one(value)
            
            for item in answers:
                if "id" not in item:
                    result[item]=answers[item]
            return result
        else:
            return result
    @classmethod
    def getReadingReviewForTPOSet(cls,userid,setid,mode):
        """
        获取学生的阅读部分答案，包括index、stem、答案
        """
        result=[]
        value={}
        value[configure.answer_userid]=int(userid)
        collection=cls.db[cls.getCollectionName(setid,mode)]
        count=collection.count(value)
        #如果找到
        if count==1:
            student_answers=collection.find_one(value)
            answers={}
            officlial_answers=cls.queryAnswerForTPOSet(configure.answer_officialid,setid,configure.answer_officialmode)
            for index in officlial_answers:
                if index.startswith('R'):
                    #如果答案有的话
                    if student_answers.has_key(index):
                        answers[index]=student_answers[index]
                    #如果没有答案
                    else:
                        answers[index]=""
            #统计结束进行排序
            sorted_result=sortDict(answers)
            for answer in sorted_result:
                single_answer={}
                single_answer["index"]=answer.keys()[0]
                single_answer["option"]=answer.values()[0]
                single_answer["stem"]=selection_questionDAO.getSelectionQuestion(setid,answer.keys()[0])["stem"]
                result.append(single_answer)

            return result


        else:
            return result
                    
    @classmethod
    def getStudentAnswerStatus(cls,userid,mode):
        """
        获取学生答题状态，对于自己买的题是否做了
        Args:
            userid:用户id
            mode:什么模式，例如exam or practice
        Return:
            如果是exam模式，就返回[{20170603:1},{20160525:0}]
            如果是practice模式，就返回[{20170603:[1,1,1,1]}]
            其中1表示做了，0表示没做
        """
        status=[]
        questions=studentInfoDAO.getQuestionSetOfSingleStudent(userid)
        # print questions
        #如果学生没有题,就直接返回
        if questions==configure.FAIL_CODE:
            return status

        #如果学生有题
        if cmp(mode,"exam")==0:
            mode=configure.answer_exammode
        else:
            mode=configure.answer_practicemode
        #然后查看相应的题库中是否有他的答案

        #如果是练习模式
        if mode==configure.answer_practicemode:
            for question in questions:
                #获取到答案
                result=cls.queryAnswerForTPOSet(userid,question,mode)
                print result
                singleStatus={}
                singleStatus["title"]=question
                #如果没有答案，就设置为空
                if result==None:
                    singleStatus["status"]=[configure.FAIL_CODE,configure.FAIL_CODE,configure.FAIL_CODE,configure.FAIL_CODE]
                #如果有答案
                else:
                    #便利答案进行查找
                    dict=[]
                    for item in result:
                        #如果判断完了，就跳出去
                        if len(dict)==4:
                            break
                        #是否有阅读题
                        if item.startswith('R'):
                            dict.append('R')
                            continue
                        #是否做了听力题
                        if item.startswith('L'):
                            dict.append('L')
                            continue
                        #是否做了口语题
                        if item.startswith('S'):
                            dict.append('S')
                            continue
                        #是否做了写作题
                        if item.startswith('W'):
                            dict.append('W')
                            continue
                    #统计结束，现在进行插入
                    singleStatus["status"]=[]
                    if 'R' in dict:
                        singleStatus["status"].append(configure.SUCCESS_CODE)
                    else:
                        singleStatus["status"].append(configure.FAIL_CODE)
                    if 'L' in dict:
                        singleStatus["status"].append(configure.SUCCESS_CODE)
                    else:
                        singleStatus["status"].append(configure.FAIL_CODE)
                    if 'S' in dict:
                        singleStatus["status"].append(configure.SUCCESS_CODE)
                    else:
                        singleStatus["status"].append(configure.FAIL_CODE)
                    if 'W' in dict:
                        singleStatus["status"].append(configure.SUCCESS_CODE)
                    else:
                        singleStatus["status"].append(configure.FAIL_CODE) 

                    #插入数据
                status.append(singleStatus)
            return status



        #如果是模考模式
        for question in questions:
            print question
            result=cls.queryAnswerForTPOSet(userid,question,mode)
            print result
            singleStatus={}
            singleStatus["title"]=question
            if len(result)==0:
                singleStatus["status"]=configure.FAIL_CODE
            else:
                singleStatus["status"]=configure.SUCCESS_CODE
            status.append(singleStatus)
        return status




if __name__=='__main__':
    asw=answer("20170603","W1","1","1")
    answerDAO.index(asw,configure.answer_practicemode)
    # asw=answer("20170603","L1","C","1")
    # answerDAO.index(asw,configure.answer_practicemode)
    # asw=answer("20170603","R3","D","1")
    # answerDAO.index(asw,configure.answer_exammode)
    # asw=answer("20170603","L3","A","1")
    # answerDAO.index(asw,configure.answer_exammode)
    # print answerDAO.querySingleAnswer(1,"20170603","R3",configure.answer_practicemode)
    # print answerDAO.queryAnswerForTPOSet(1,"20170603",configure.answer_practicemode)
    # answerDAO.clearAllAnswers(1)
    print answerDAO.getStudentAnswerStatus(1,"practice")
    # print answerDAO.clearAnswersForQuestionSet(1,20170603,"exam","Reading")
    # print answerDAO.getReadingReviewForTPOSet(1,20170603,"exam")
