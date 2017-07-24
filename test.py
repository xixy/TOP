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
from selection_questionDAO import selection_questionDAO
from answerDAO import answerDAO
from answer import answer
import configure
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

@app.route('/login',methods=['GET'])
def login():
    # username=request.data[username]
    # password=request.data[password]
    username="xixiangyu"
    password=123456
    result=studentInfoDAO.valid(username,password)
    return jsonify({"id":result}),201

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
def saveanswer():
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

# app.add_url_rule('/login',login())
if __name__ == '__main__':
    app.run(debug=True)
