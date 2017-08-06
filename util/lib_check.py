# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../model/')
sys.path.append('../configure/')

import pymongo

from configure import ip,port
import configure
from selection_question import selection_question
client=pymongo.MongoClient(ip,port)
db=client.questions
collectionlist=db.collection_names()

def check():
    """
    检查Reading的部分的type是否正确
    """
    for collectionname in collectionlist:
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

        if configure.writing_stem not in question.keys():
            print "写作题第一题没有题干："+collectionname
        if configure.writing_article not in question.keys():
            print "写作题第一题没有文章："+collectionname
        if configure.writing_record not in question.keys():
            print "写作题第一题没有听力文本："+collectionname
        #查找第二题
        value={configure.index:"W2"}
        if collection.find(value).count()==0:
            print "写作题第二题不存在："+collectionname
            continue
        question=collection.find_one(value)
        if configure.writing_stem not in question.keys():
            print "写作题第二题没有题干："+collectionname


if __name__ == '__main__':
    check()
