# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

class score(object):
    """一套题的评分，需要记录学生、TPO1、什么模式
    """
	
    def __init__(self,setid,userid,mode):
    	self.setid=setid #例如TPO1，表示哪套题
        self.userid=userid # 例如1，表示学生1
        self.mode=mode# 例如练习模式，模考模式等
        pass