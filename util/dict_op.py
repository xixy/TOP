# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

def sortDict(mydict):
    """
    对R1、R12、R3这样排序，得到结果是R1、R3、R12
    Args:
        mydict:一个dict，例{'R1':C,'R2':D,'R12':E}
    Return:
        一个list
    """
    return [{key:mydict[key]} for key in sorted(mydict.keys(),key=lambda x:int(x[1:]))]