# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

#mongodb的配置
ip="127.0.0.1"
port=27017

#标示文件夹名称
Reading="Reading"
Listening="Listening"
Speaking="Speaking"
Writting="Writting"
#标示答案文件
Answer="answer"

#标示数据库中存入的样子

ReadingMark="R"
ListeningMark="L"
SpeakingMark="S"
WrittingMark="W"

Mark={Reading:ReadingMark,Listening:ListeningMark,Speaking:SpeakingMark,Writting:WrittingMark}

#选择题在数据库中的格式
selection_stem="stem"
selection_options="options"
#所有题都存index
index="index"

#学生信息的表
student_name="username"#学生名称
student_password="password"#学生密码
student_id="id"#学生账号
student_questions="questions"#学生所能做的题
student_classid="classid"

#管理员信息的表
admin_name="username"#学生名称
admin_password="password"#学生密码
admin_id="id"#学生账号

#返回码
FAIL_CODE=-1
SUCCESS_CODE=1

#答案相关的配置
answer_practicemode="_practice"
answer_exammode="_exam"
answer_officialmode="_official"
answer_officialid=-1
answer_userid="userid"

#跟数据库中存的内容相关
LineBreakMark="<br>"

#题的类型
question_type="question_type"
single_selection_type="single_selection_type"
insert_selection_type="insert_selection_type"
r_multiple_selection_type="r_multiple_selection_type"
l_multiple_selection_type="l_multiple_selection_type"
isLast="isLast"

#存题的collection的前缀
question_prefix="TPO"
answer_prefix="TPO"