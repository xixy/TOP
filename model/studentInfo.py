# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

class studentInfo(object):
    """学生信息，包括id、姓名、密码，学生能做的题，学生的班级id（默认为0)"""

    
    def __init__(self,id,username,password,classid=0):
        self.id=int(id)
        self.username=username
        self.password=password
        self.questions=[]
        self.classid=classid
        pass


