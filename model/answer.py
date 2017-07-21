# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

class answer(object):
    """一道题的答案"""
	
    def __init__(self,setid,index,choice,userid):
    	self.setid=setid #例如TPO1，表示哪套题
        self.index=index # 例如R1，表示哪道题
        self.choice=choice# 例如A，表示学生选择
        self.userid=userid # 例如1，表示学生1
        pass


