# coding: utf-8
#!flask/bin/python

from flask import Flask, jsonify
from flask import request
from flask import send_file,send_from_directory
from flask_cors import *
import os
import pymongo
import sys
reload(sys)
sys.path.append('./dao/')
sys.path.append('./model/')
sys.path.append('./util')
sys.path.append('./configure')

sys.setdefaultencoding('utf-8')
from studentInfoDAO import studentInfoDAO
from adminDAO import adminDAO
from selection_questionDAO import selection_questionDAO
from answerDAO import answerDAO
from answer import answer
import configure


import time
 
#产生子进程，而后父进程退出
pid = os.fork()
if pid > 0:
    sys.exit(0)
 
#修改子进程工作目录
os.chdir("/")
#创建新的会话，子进程成为会话的首进程
os.setsid()
#修改工作目录的umask
os.umask(0)
 
#创建孙子进程，而后子进程退出
pid = os.fork()
if pid > 0:
    sys.exit(0)
 
#重定向标准输入流、标准输出流、标准错误
sys.stdout.flush()
sys.stderr.flush()
si = file("/dev/null", 'r')
so = file("/dev/null", 'a+')
se = file("/dev/null", 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

@app.route('/login',methods=['POST'])
def login():
    username=request.data[username]
    password=request.data[password]
    username="xixiangyu"
    password=123456
    result=studentInfoDAO.valid(username,password)
    return jsonify({"id":result}),201

@app.route('/admin/login',methods=['POST'])
def adminLogin():
    """
    管理员登陆验证
    """
    username=request.data[username]
    password=request.data[password]
    username="xixiangyu"
    password=123456
    result=adminDAO.valid(username,password)
    return jsonify({"id":result}),201

@app.route('/student/all',methods=['GET'])
def getAllStudents():
    """
    查看所有学生信息
    """
    result=studentInfoDAO.getAllStudents()
    print result
    # result={"1":{"id":1,"questions":["1","2","3"]}}
    return jsonify(result),201

@app.route('/download/<filename>',methods=['GET'])
def download(filename):
    directory=os.getcwd()
    return send_from_directory(directory,filename,as_attachment=True)

@app.route('/question/<setid>/<index>',methods=['GET'])
def getQuestion(setid,index):
	"""
	获取题库的某套题
	Args:
		setid:某套题，例如TPO1
		index:第几个题，例如R13

	"""
	questions=selection_questionDAO.getSelectionQuestion(setid,index)
	return jsonify(questions),201

@app.route('/status/<userid>/<mode>',methods=['GET'])
def getQuestionStatus(userid,mode):
    """
    获取到某个学生的题的状态
    """
    #先获取到学生的所有的题
    status={}
    questions=studentInfoDAO.getQuestionsOfSingleStudent(userid)
    if cmp(mode,"exam")==0:
        mode=configure.answer_exammode
    else:
        mode=configure.answer_practicemode
    #然后查看相应的题库中是否有他的答案
    print questions
    for question in questions:
        result=answerDAO.queryAnswerForTPOSet(1,question,mode)
        print result
        if result==None:
            status[question]=configure.FAIL_CODE
        else:
            status[question]=configure.SUCCESS_CODE
    return jsonify(status),201


@app.route('/answer/<setid>/<index>',methods=['GET'])
def getOfficialAnswer(setid,index):
    """
    获取某套题某个题的标准答案
    Args:
        setid:某套题，例如TPO1
        index:第几个题，例如R13
    """
    result=answerDAO.querySingleAnswer(configure.answer_officialid,setid,index,configure.answer_officialmode)
    return jsonify(result),201

@app.route('/studentanswer/<userid>/<setid>/<index>/<mode>',methods=['GET'])
def getStudentAnswer(mode,userid,setid,index):
    """
    获取某个学生某套题某个题的答案
    Args:
        setid:某套题，例如TPO1
        index:第几个题，例如R13
    """
    if cmp(mode,"exam")==0:
        mode=configure.answer_exammode
    else:
        mode=configure.answer_practicemode

    result=answerDAO.querySingleAnswer(userid,setid,index,mode)
    return jsonify(result),201

@app.route('/answer/submit',methods=['POST'])
def saveAnswer():
    """
    学生提交答案

    """
    setid=request.data["setid"]
    index=request.data["index"]
    userid=request.data["userid"]
    options=request.data["options"]
    asw=answer(setid,index,options,userid)
    mode=request.data["mode"]
    if cmp(mode,"exam")==0:
        mode=configure.answer_exammode
    else:
        mode=configure.answer_practicemode   
	answerDAO.index(asw,mode)
	return jsonify({"message":"ok"}),201

@app.route('/answer',methods=['DELETE'])
def deleteAnswer():
    """
    删除某套题的答案
    """
    setid=request.data["setid"]
    userid=request.data["userid"]
    mode=request.data["mode"]
    if cmp(mode,"exam")==0:
        mode=configure.answer_exammode
    else:
        mode=configure.answer_practicemode
    answerDAO.clearAnswersForQuestionSet(userid,setid,mode)

# app.add_url_rule('/login',login())
if __name__ == '__main__':
    app.run('0.0.0.0')
