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

sys.setdefaultencoding('utf-8')
from studentInfoDAO import studentInfoDAO
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

@app.route('/login',methods=['GET'])
def login():
    # username=request.form[username]
    # password=request.form[password]
    username="xixiangyu"
    password=123456
    result=studentInfoDAO.valid(username,password)
    return jsonify({"id":result}),201

@app.route('/download/<filename>',methods=['GET'])
def download(filename):
    directory=os.getcwd()
    return send_from_directory(directory,filename,as_attachment=True)
# app.add_url_rule('/login',login())
if __name__ == '__main__':
    app.run(debug=True)
