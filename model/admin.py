# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

class admin(object):
    """ 管理员信息，包括id、用户名、密码"""

    
    def __init__(self,id,username,password):
        self.id=int(id)
        self.username=username
        self.password=password
        pass


