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
client=pymongo.MongoClient(ip,port)
db=client.questions
collectionlist=db.collection_names()

def check_reading_type():
    """
    检查Reading的部分的type是否正确
    """
    for collectionname in collectionlist:
        collection=db[collectionname]
        #查找Reading插入题的数量
        value={configure.question_type:configure.insert_selection_type}
        count=collection.find(value).count()
        if count>3:
            print "阅读题插入题数量大于3个:"+collectionname+":"+str(count)
        if count<2:
            print "阅读题插入题数量小于2个:"+collectionname+":"+str(count)

        #查找Reading多选题的数量
        value={configure.question_type:configure.r_multiple_selection_type}
        count=collection.find(value).count()
        if count>3:
            print "阅读题多选题数量大于3个："+collectionname+":"+str(count)
        if count<2:
            print "阅读题多选题数量小于2个："+collectionname+":"+str(count)

        #查找听力多选题
        value={configure.question_type:configure.l_multiple_selection_type}
        count=collection.find(value).count()
        if count>3:
            print "听力题多选题数量大于3个："+collectionname+":"+str(count)


if __name__ == '__main__':
    check_reading_type()