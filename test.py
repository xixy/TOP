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

@app.route('/getquestions/<setid>/<index>',methods=['GET'])
def getquestions(setid,index):
	"""
	获取题库的某套题
	Args:
		setid:某套题，例如TPO1
		index:第几个题，例如R13

	"""
	questions=selection_questionDAO.getSelectionQuestion(setid,index)
	return jsonify(questions),201

@app.route('/saveanswer/<setid>/<index>/<userid>/<options>/<mode>',methods=['GET'])
def saveanswer(setid,index,userid,options,mode):
	asw=answer(setid,index,options,userid)
	print "here"
	answerDAO.index(asw,mode)
	return jsonify({"message":"ok"}),201

# app.add_url_rule('/login',login())
if __name__ == '__main__':
    app.run(debug=True)
