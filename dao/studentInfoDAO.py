#! /usr/local/bin/python

import sys
sys.path.append('../model/')
import pymongo
from studentInfo import studentInfo
from bson import json_util as jsonb
from dbop import ip,port
class studentInfoDAO(object):
    client=pymongo.MongoClient(ip,port)
    db=client.test
    collection=db.studentinfo
    def __init__(self):
        pass
    @classmethod
    def index(cls,studentInfo):
        value={}
        value['id']=studentInfo.id
    	value['username']=studentInfo.username
    	value['password']=studentInfo.password
        cls.collection.insert(value)
        for data in cls.collection.find():
        	print data
    @classmethod
    def delete(cls,studentInfo):
        value={}
        value['id']=studentInfo.id
    	value['username']=studentInfo.username
        cls.collection.find_one_and_delete(value)
        for data in cls.collection.find():
        	print data

    @classmethod
    def valid(cls,username,password):
        value={}
    	value["username"]=username
    	value["password"]=password
    	count = cls.collection.count(value)
    	if count==1:
    		for i in cls.collection.find(value):
    			return i["id"]
    	else:
    		return -1

if __name__=='__main__':
    studentInfo=studentInfo(1,"anxiao",123456)
    studentInfoDAO.index(studentInfo)
    print studentInfoDAO.valid("anxiao",123456)
    studentInfoDAO.delete(studentInfo)
