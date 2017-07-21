# coding: utf-8
#!flask/bin/python

import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def login():
    client=pymongo.MongoClient('127.0.0.1',27017)
    db=client.test
    collection=db.studentinfo
    user={"name":"anxiao","password":"1234567"}
    collection.insert(user)
    for data in collection.find():
        print data



if __name__ == '__main__':
    login()
