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
from writing_question_extractor import writing_question_extractor
from listening_text_extractor import listening_text_extractor
from writing_questionDAO import writing_questionDAO



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
		listening_question_files_path=[]
		listening_text_files_path=[]
		speaking_files_path=[]
		writing_files_path=[]
		answer_file_path=''

		#存储题目个数，然后用于检查是否能够对应上
		reading_questions_count=[]
		listening_questions_count=[]

		reading_answers_count=[]
		listening_answers_count=[]
		#分类统计
		for filepath in filepaths:
			if ".DS_Store" in filepath:
				continue
			if ".docx" in filepath:
				continue
			#取出阅读部分
			if configure.Reading in filepath:
				reading_files_path.append(filepath)
				continue
			
			#取出听力题目部分
			if configure.Listening in filepath and configure.ListeningQuestions in filepath:
				listening_question_files_path.append(filepath)
				continue
			#取出听力文本部分
			if configure.Listening in filepath and configure.ListeningText in filepath:
				listening_text_files_path.append(filepath)
				continue			


			#取出口语部分
			if configure.Speaking in filepath:
				speaking_files_path.append(filepath)
				continue

			#取出写作部分
			if configure.Writting in filepath:
				writing_files_path.append(filepath)
				continue

			#取出答案部分
			if configure.Answer in filepath:
				answer_file_path=filepath
				continue


		
		questions_json=[]#存放所有的选择题

		
		#提取阅读中的选择题
		reading_files_path.sort()
		question_list=[]
		#检查文件数量
		if len(reading_files_path)!=3:
			print "阅读题文件不等于3:"+str(setid)

		for filepath in reading_files_path:
			# print filepath
			questions=selection_question_extractor.getSelectionQuestions(filepath)
			reading_questions_count.append(len(questions))
			if len(questions)<14:
				print "阅读题目少于14："+filepath+":"+str(len(questions))
			if len(questions)>14:
				print "阅读题目大于14："+filepath+":"+str(len(questions))
			# print questions

			question_list.extend(questions)

		reading_questions_json=selection_question.getSetQuestion(question_list,configure.Reading)
		questions_json.extend(reading_questions_json)# 加入到总题目中
		
		

		#提取听力中的选择题
		question_list=[]
		listening_question_files_path.sort()
		#检查文件数量
		if len(listening_question_files_path)!=6:
			print "听力题题目文件不等于6:"+str(setid)

		for filepath in listening_question_files_path:
			questions=selection_question_extractor.getSelectionQuestions(filepath)
			listening_questions_count.append(len(questions))
			if len(questions)<5:
				print "听力题目少于5："+filepath+":"+str(len(questions))
			if len(questions)>6:
				print "听力题目大于6："+filepath+":"+str(len(questions))
			question_list.extend(questions)

		listening_questions_json=selection_question.getSetQuestion(question_list,configure.Listening)
		questions_json.extend(listening_questions_json)# 加入到总题目中



		#处理听力中的录音文本

		#检查文件数量
		if len(listening_text_files_path)!=6:
			print "听力题听力文本文件不等于6:"+str(setid)

		listening_text_files_path.sort()
		for filepath in listening_text_files_path:
			text=listening_text_extractor.getListeningText(filepath)
			questions_json.append(text)

		#对选择题进行持久化存储
		selection_questionDAO.indexQuestions(setid,questions_json)

		#处理口语

		#检查文件数量
		if len(speaking_files_path)!=6:
			print "口语题文件不等于6:"+str(setid)

		speaking_files_path.sort()
		for filepath in speaking_files_path:
			# print filepath
			#提取口语
			question=speaking_question_extractor.getSpeakingQuestion(filepath)

			#持久化
			speaking_questionDAO.indexQuestions(setid,question)

		#处理写作
		#检查文件数量
		if len(writing_files_path)!=2:
			print "写作题文件不等于2:"+str(setid)

		writing_files_path.sort()
		for filepath in writing_files_path:
			#提取写作
			question=writing_question_extractor.getWritingQuestion(filepath)
			#持久化
			writing_questionDAO.indexQuestions(setid,question)


		#处理答案
		answers_count=answer_saver.indexAnswerForSingleSet(answer_file_path,setid)

		#进行检查，是否能够对应上
		reading_answers_count=answers_count[0]
		listening_answers_count=answers_count[1]

		if reading_answers_count!=reading_questions_count:
			print "阅读题答案和问题个数对应不上"+str(setid)
			print reading_answers_count
			print reading_questions_count
		if listening_answers_count!=listening_questions_count:
			print "听力题答案和问题个数对应不上"+str(setid)
			print listening_answers_count
			print listening_questions_count


		pass





	
