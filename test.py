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
from report_generator import report_generator
from answerDAO import answerDAO
from answer import answer
from studentInfo import studentInfo
import configure
from ip_limit import isAllowedIP

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

#学生登陆
@app.route('/login',methods=['POST'])
def login():
    ip=request.remote_addr
    if not isAllowedIP(ip):
        return jsonify({"id":-1}),401

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
    查看所有学生信息,得到学生id、用户名、密码、学生买的题
    """
    result=studentInfoDAO.getAllStudents()
    return jsonify(result),200

#管理员添加学生
@app.route('/student',methods=['POST'])
def addStudent():
    """
    添加学生，需要提供用户名、密码、班级、题目（可为空）
    """
    data=request.get_json()
    username=data[configure.student_login_username]
    password=data[configure.student_login_password]
    classid=data[configure.student_classid]
    questions=data[configure.student_questions]

    #先创建学生
    student=studentInfo(username,password,classid)
    id=studentInfoDAO.index(student)
    #然后给学生添加题目
    studentInfoDAO.addQuestionSetsForStudent(id,questions)
    return jsonify({"message":"ok"}),200

#管理员删除学生
@app.route('/student',methods=['DELETE'])
def deleteStudent():
    """
    删除学生，需要提供id
    """
    data=request.get_json()
    student_id=data[configure.student_id]
    studentInfoDAO.delete(student_id)
    return jsonify({"message":"ok"}),200

#管理员给学生添加题目
@app.route('/student/question',methods=['POST'])
def addQuestionForStudent():
    """
    给学生添加题目，需要提供id和题目list
    """
    data=request.get_json()
    id=data[configure.student_id]
    questions=data[configure.student_questions]
    studentInfoDAO.addQuestionSetsForStudent(id,questions)
    return jsonify({"message":"ok"}),200

@app.route('/download/<filename>',methods=['GET'])
def download(filename):
    directory=os.getcwd()
    return send_from_directory(directory,filename,as_attachment=True)

#获取所有的题setid，用于管理员添加题目页面
@app.route('/question/all',methods=['GET'])
def getAllQuestion():
    """
    获取所有的题setid，用于管理员添加题目页面
    """
    questions=selection_questionDAO.getAllQuestionSetid()
    return jsonify(questions),200

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


#生成报告
@app.route('/report',methods=['POST'])
def generatReport():
    """
    生成报告
    """
    data=request.get_json()
    setid=data["setid"]
    userid=data["userid"]
    mode=data["mode"]
    student=studentInfoDAO.getStudentInfoById(userid)
    username=student[configure.student_name]
    directory=answer_path+str(username)+"/"+mode+"/"+str(setid)
    #先创建文件夹，如果文件夹不存在
    if not os.path.exists(directory):
        os.makedirs(directory)
    #然后保存文件
    path=directory+"/"+"report"+".txt"
    print path
    status=report_generator.generatReport(userid,setid,mode,path)
    return jsonify(status),200

#获取报告
@app.route('/report/<userid>/<setid>',methods=['GET'])
def getReport(userid,setid):
    """
    第三个页面，用来返回报告
    """
    result=answerDAO.getAnswerForReport(setid,userid,"exam")
    if result==[]:
        return jsonify({"message":"no"}),500
    else:
        return jsonify(result),200


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
def getStudentSingleAnswer(mode,userid,setid,index):
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

#获取学生某套题某个题的答案
@app.route('/studentanswer/review/<userid>/<setid>/<mode>',methods=['GET'])
def getStudentReadingReviewsForSet(userid,setid,mode):
    """
    获取学生阅读题的答案和题干
    Args:
        setid:某套题，例如TPO1
        userid:学生id
        mode：模式
    """
    result=answerDAO.getReadingReviewForTPOSet(userid,setid,mode)
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
    mode=data["mode"]
    #如果是选择题
    if "R" in index or "L" in index:
        options=data["options"]
        asw=answer(setid,index,options,userid)
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
                f.write(line+'\n')
            f.close()
            #在数据库中进行标记
            asw=answer(setid,index,str(1),userid)
            if cmp(mode,"exam")==0:
                mode=configure.answer_exammode
            else:
                mode=configure.answer_practicemode   
            answerDAO.index(asw,mode)

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
    app.run('0.0.0.0',port=5000)
