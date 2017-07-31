# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../configure/')
sys.path.append('../model/')
sys.path.append('../dao/')
import configure
from selection_question_extractor import selection_question_extractor
from filepath import getFullFilePath
from selection_question import selection_question
from selection_questionDAO import selection_questionDAO
from answer_saver import answer_saver
from speaking_question_extractor import speaking_question_extractor
from speaking_questionDAO import speaking_questionDAO


class question_saver(object):
	"""将所有题库倒入到数据库中"""


	@classmethod
	def savequestions(cls,setid,filepaths):
		"""
		对一套题进行存储
		Args:
			filepaths:这套题的所有文件路径
			setid:这套题的名称，例如20170603


		"""
		reading_files_path=[]
		listening_files_path=[]
		speaking_files_path=[]
		writting_files_path=[]
		answer_files_path=[]
		#分类统计
		for filepath in filepaths:
			if ".DS_Store" in filepath:
				continue
			#取出阅读部分
			if configure.Reading in filepath:
				reading_files_path.append(filepath)
				continue
			
			#取出听力部分
			if configure.Listening in filepath:
				listening_files_path.append(filepath)
				continue

			#取出口语部分
			if configure.Speaking in filepath:
				speaking_files_path.append(filepath)
				continue

			#取出写作部分
			if configure.Writting in filepath:
				writting_files_path.append(filepath)
				continue
			writting_files_path.sort()
			#取出答案部分
			if configure.Answer in filepath:
				answer_files_path.append(filepath)
				continue


		
		questions_json=[]#存放所有的选择题

		
		#提取阅读中的选择题
		reading_files_path.sort()
		question_list=[]
		for filepath in reading_files_path:
			# print filepath
			questions=selection_question_extractor.getSelectionQuestions(filepath)
			if len(questions)<13:
				print "题目少于13："+filepath+":"+str(len(questions))
			if len(questions)>14:
				print "题目大于14："+filepath+":"+str(len(questions))
			# print questions

			question_list.extend(questions)

		reading_questions_json=selection_question.getSetQuestion(question_list,configure.Reading)
		questions_json.extend(reading_questions_json)# 加入到总题目中
		"""

		#提取听力中的选择题
		question_list=[]
		listening_files_path.sort()

		for filepath in listening_files_path:
			questions=selection_question_extractor.getSelectionQuestions(filepath)
			question_list.extend(questions)
		"""



		# listening_questions_json=selection_question.getSetQuestion(question_list,configure.Listening)
		# questions_json.extend(listening_questions_json)# 加入到总题目中


		#进行持久化存储
		selection_questionDAO.indexQuestions(setid,questions_json)

		#处理口语
		speaking_files_path.sort()
		for filepath in speaking_files_path:
			print filepath
			question=speaking_question_extractor.getSpeakingQuestion(filepath)
			speaking_questionDAO.indexQuestions(setid,question)



		#处理答案
		answer_saver.indexAnswerForMultiSet(answer_files_path,setid)
	

		pass





	
