# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import re

student_ip_pattern=re.compile(r'124+\.+205+\.') #匹配可用的ip

def isAllowedIP(ip,pattern):
    """
    查看ip是否可用
    Args:
        is:需要查询的ip
    Return:
        如果可以，就反悔Ture，否则False
    """
    match=pattern.search(ip)
    if match:
        return True
    else:
        return False

if __name__ == '__main__':
    print isAllowedIP('124.205.77.199',student_ip_pattern)
