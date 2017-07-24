# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../model/')
sys.path.append('../configure/')
import pymongo
from admin import admin
from bson import json_util as jsonb
import configure
class adminDAO(object):
    """学生信息的持久化"""

    client=pymongo.MongoClient(configure.ip,configure.port)
    db=client.users#db
    collection=db.admin#collection
    def __init__(self):
        pass

    @classmethod
    def index(cls,admin):
        """保存管理员信息到数据库中
        Args:
            admin:管理员信息
        Return:
            None
        """
        value={}
        value[configure.admin_id]=admin.id
        value[configure.admin_name]=admin.username
        value[configure.admin_password]=admin.password
        cls.collection.insert(value)


    @classmethod
    def delete(cls,admin):
        """删除管理员信息"""
        value={}
        value[configure.admin_id]=admin.id
        value[configure.admin_name]=admin.username
        cls.collection.remove(value)

    @classmethod
    def valid(cls,username,password):
        """验证管理员
        Args:
            username:管理员用户名
            password:学生密码
        Return:
            如果验证成功，返回学生id
            否则返回configure.FAIL_CODE
        """
        value={}
        value[configure.admin_name]=username
        value[configure.admin_password]=password
        count = cls.collection.count(value)
        if count==1:
            for i in cls.collection.find(value):
                return i[configure.admin_id]
        else:
            return configure.FAIL_CODE

if __name__ == '__main__':
    admin1=admin("1","xxy","123456")
    adminDAO.index(admin1)
    print adminDAO.valid("xxy","123456")
    # adminDAO.delete(admin1)