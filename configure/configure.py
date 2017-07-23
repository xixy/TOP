# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

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

#返回码
FAIL_CODE=-1

#答案相关的配置
answer_practicemode="_practice"
answer_exammode="_exam"
answer_officialmode="_official"
answer_officialid=-1
answer_userid="userid"

#跟数据库中存的内容相关
LineBreakMark="<br>"