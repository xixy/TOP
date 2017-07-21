# coding: utf-8
#!flask/bin/python

from flask import Flask, jsonify
from flask import request
from flask_cors import *
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

@app.route('/login',methods=['POST'])
def login():
    username=request.form[username]
    password=request.form[password]
    connection=pymongo.Connection('10.32.38.50',27017)
    db=connection.test
    collection=db.studentinfo
    user={"name":"安晓","password":"1234567"}
    collection.insert(user)
    for data in collection.find():
        print data
    return jsonify({'status':'OK'}),201



if __name__ == '__main__':
    app.run(debug=True)
