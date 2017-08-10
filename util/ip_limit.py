# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python
import re

student_ip_pattern=re.compile(r'58+\.+132+\.+205') #匹配可用的ip

def isAllowedIP(ip):
    """
    查看ip是否可用
    Args:
        is:需要查询的ip
    Return:
        如果可以，就反悔Ture，否则False
    """
    pattern=student_ip_pattern
    match=pattern.search(ip)
    if match:
        return True
    else:
        return False

if __name__ == '__main__':
    print isAllowedIP('58.132.205.130')
