#! /usr/local/bin/python

class answer(object):
    '''
    single answer for each question
    '''
    def __init__(self,setid,index,choice,userid):
    	self.setid=setid # which set 
        self.index=index # which question
        self.choice=choice
        self.userid=userid # whose answer
        pass


