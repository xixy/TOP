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


class question_saver(object):
	"""将所有题库倒入到数据库中"""


	@classmethod
	def savequestions(cls,directory):
		"""
		存储所有的题库，首先进行遍历，然后进行调用
		Args:
			directory:这套题的目录


		"""
		filepaths=[]
		reading_files_path=[]
		listening_files_path=[]
		speaking_files_path=[]
		writting_files_path=[]
		answer_files_path=[]

		getFullFilePath(directory,filepaths)
		#分类统计
		for filepath in filepaths:
			#取出阅读部分
			if configure.Reading in filepath:
				reading_files_path.append(filepath)
				continue
			reading_files_path.sort()
			#取出听力部分
			if configure.Listening in filepath:
				listening_files_path.append(filepath)
				print filepath
				continue
			listening_files_path.sort()
			print listening_files_path
			#取出口语部分
			if configure.Speaking in filepath:
				speaking_files_path.append(filepath)
				continue
			speaking_files_path.sort()
			#取出写作部分
			if configure.Writting in filepath:
				writting_files_path.append(filepath)
				continue
			writting_files_path.sort()
			#取出答案部分
			if configure.Answer in filepath:
				answer_files_path.append(filepath)
				continue


		
		questions_json=[]#存放所有的题

		
		#提取阅读中的选择题
		question_list=[]
		for filepath in reading_files_path:
			questions=selection_question_extractor.getSelectionQuestions(filepath)
			question_list.extend(questions)

		reading_questions_json=selection_question.getSetQuestion(question_list,configure.Reading)
		questions_json.extend(reading_questions_json)# 加入到总题目中

		#提取听力中的选择题
		question_list=[]
		print listening_files_path

		for filepath in listening_files_path:
			questions=selection_question_extractor.getSelectionQuestions(filepath)
			question_list.extend(questions)


		listening_questions_json=selection_question.getSetQuestion(question_list,configure.Listening)
		questions_json.extend(listening_questions_json)# 加入到总题目中


		#进行持久化存储
		selection_questionDAO.indexQuestions("20170603",questions_json)

		#处理答案部分TPO
		answer_saver.indexAnswerForMultiSet(answer_files_path,"20170603")

		

				

		pass

if __name__ == '__main__':
	question_saver.savequestions('../resources/questions/20170603')




	
