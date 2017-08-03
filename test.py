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
from speaking_questionDAO import speaking_questionDAO
from writing_questionDAO import writing_questionDAO
from answerDAO import answerDAO
from answer import answer
import configure

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

#学生登陆
@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    username=data[configure.student_login_username]
    password=data[configure.student_login_password]
    result=studentInfoDAO.valid(username,password)
    if result>0:
        return jsonify({"id":result}),200
    else:
        return jsonify({"id":result}),401

#管理员登陆验证
@app.route('/admin/login',methods=['POST'])
def adminLogin():
    """
    管理员登陆验证
    """
    data=request.get_json()
    username=data[configure.admin_login_username]
    password=data[configure.admin_login_password]
    
    result=adminDAO.valid(username,password)
    if result>0:
        return jsonify({"id":result}),200
    else:
        return jsonify({"id":result}),401

#获取所有学生信息
@app.route('/student/all',methods=['GET'])
def getAllStudents():
    """
    查看所有学生信息,得到学生id和对应的数据
    """
    result=studentInfoDAO.getAllStudents()
    print result
    return jsonify(result),200

@app.route('/download/<filename>',methods=['GET'])
def download(filename):
    directory=os.getcwd()
    return send_from_directory(directory,filename,as_attachment=True)

#获取题目信息
@app.route('/question/<setid>/<index>',methods=['GET'])
def getQuestion(setid,index):
    """
    获取题库的某套题
    Args:
        setid:某套题，例如TPO1
	index:第几个题，例如R13
    """
    #如果是阅读、听力题
    if "R" in index or "L" in index:
        question=selection_questionDAO.getSelectionQuestion(setid,index)
    else:
        #如果是口语题
        if "S" in index:
            question=speaking_questionDAO.getQuestion(setid,index)
        else:
            #如果是写作题
            if "W" in index:
                question=writing_questionDAO.getQuestion(setid,index)
    return jsonify(question),200

#查看学生答题信息
@app.route('/status/<userid>/<mode>',methods=['GET'])
def getQuestionStatus(userid,mode):
    """
    获取到某个学生的题的状态
    """
    status=answerDAO.getStudentAnswerStatus(userid,mode)
    return jsonify(status),200

#获取标准答案
@app.route('/answer/<setid>/<index>',methods=['GET'])
def getOfficialAnswer(setid,index):
    """
    获取某套题某个题的标准答案
    Args:
        setid:某套题，例如TPO1
        index:第几个题，例如R13
    """
    result=answerDAO.querySingleAnswer(configure.answer_officialid,setid,index,configure.answer_officialmode)
    return jsonify(result),200

#获取学生某套题某个题的答案
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
    return jsonify(result),200


answer_path="../Answer/"
#保存学生提交的答案:包括选择题、写作题
@app.route('/answer/submit',methods=['POST'])
def saveAnswer():
    """
    学生提交答案

    """
    data=request.get_json()
    setid=data["setid"]
    index=data["index"]
    userid=data["userid"]
    #如果是选择题
    if "R" in index or "L" in index:
        options=data["options"]
        asw=answer(setid,index,options,userid)
        mode=data["mode"]
        if cmp(mode,"exam")==0:
            mode=configure.answer_exammode
        else:
            mode=configure.answer_practicemode   
        answerDAO.index(asw,mode)
    else:
        #如果是写作题
        if "W" in index:
            options=data["options"]
            #如果文件夹不存在，就创建文件夹
            student=studentInfoDAO.getStudentInfoById(userid)
            username=student[configure.student_name]
            directory=answer_path+username+"/"+mode+"/"+str(setid)
            if not os.path.exists(directory):
                os.makedirs(directory)

            #保存作文
            path=directory+"/"+str(index)+".txt"
            f=open(path,'w')
            for line in options:
                f.write(line)
            f.close()

    return jsonify({"message":"ok"}),200




#保存学生提交的听力答案，存储为
#Answer/username/exam/20170603/S1.wav
#Answer/username/exam/20170603/W1.txt
@app.route('/upload/<userid>/<setid>/<index>/<mode>',methods=['POST'])
def upload_record(userid,setid,index,mode):
    #存储答案文件
    upload_files=request.files.getlist("record")
    student=studentInfoDAO.getStudentInfoById(userid)
    username=student[configure.student_name]
    directory=answer_path+username+"/"+mode+"/"+str(setid)
    #先创建文件夹，如果文件夹不存在
    if not os.path.exists(directory):
        os.makedirs(directory)
    #然后保存文件
    path=directory+"/"+str(index)+".wav"
    for file in upload_files:
        file.save(path)
    #在数据库中进行标记
    asw=answer(setid,index,str(1),userid)
    if cmp(mode,"exam")==0:
        mode=configure.answer_exammode
    else:
        mode=configure.answer_practicemode   
    answerDAO.index(asw,mode)
    #返回ok
    return jsonify({"message":'ok'}),200



#删除学生某个题答案
@app.route('/answer',methods=['DELETE'])
def deleteAnswer():
    """
    删除某套题的答案
    """
    data=request.get_json()
    setid=data["setid"]
    userid=data["userid"]
    mode=data["mode"]
    part=data["part"]
    if cmp(mode,"exam")==0:
        mode=configure.answer_exammode
    else:
        mode=configure.answer_practicemode
    answerDAO.clearAnswersForQuestionSet(userid,setid,mode,part)
    return jsonify({"message":"ok"}),200

# app.add_url_rule('/login',login())
if __name__ == '__main__':
    app.run('0.0.0.0')
