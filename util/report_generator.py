# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../configure/')
sys.path.append('../model/')
sys.path.append('../dao/')
import configure
from studentInfoDAO import studentInfoDAO
from answerDAO import answerDAO
from selection_questionDAO import selection_questionDAO

def sortDict(mydict):
    """
    对R1、R12、R3这样排序，得到结果是R1、R3、R12
    Args:
        mydict:一个dict，例{'R1':C,'R2':D,'R12':E}
    Return:
        一个list
    """
    return [{key:mydict[key]} for key in sorted(mydict.keys(),key=lambda x:int(x[1:]))]

class report_generator(object):
    """用于生成客观题报告"""

    @classmethod
    def calculateScoreForListening(cls,listening_answers,official_answers):
        """
        计算听力部分的最终得分
        Args:
            listening_answers:听力题答案
            official_answers:标准答案
        """
        pass

    @classmethod
    def calculateScoreForReading(cls,reading_answers,official_answers):
        """
        计算听力部分的最终得分
        Args:
            reading_answers:阅读题答案
            official_answers:标准答案
        """
        pass       

    

    @classmethod
    def writeReport(cls,reading_answers,listening_answers,official_answers,report_path):
        """
        生成报告正文，包括阅读和听力
        Args:
            reading_answers:阅读题答案
            listening_answers:听力题答案
            report_path:报告的路径
            official_answers:标准答案
        """
        f=open(report_path,'w')
        count=0


        #先写阅读题答案
        for single_reading_answers in reading_answers:
            count+=1
            #进行排序
            single_reading_answers=sortDict(single_reading_answers)
            #构造一行答案
            answer_line=""
            official_answer_line=""
            for single_answer in single_reading_answers:
                print single_answer
                answer_line=answer_line+single_answer.values()[0]+","
                official_answer_line=official_answer_line+official_answers[single_answer.keys()[0]]+","
            #写学生答案
            f.write(configure.report_reading+str(count)+"\n"+answer_line[:-1]+"\n")
            #写标准答案
            f.write(official_answer_line[:-1]+"\n")

        #写听力题答案
        count=0
        for single_listening_answers in listening_answers:
            count+=1
            #进行排序
            single_listening_answers=sortDict(single_listening_answers)
            #构造一行答案
            answer_line=""
            official_answer_line=""
            for single_answer in single_listening_answers:
                # print single_answer
                answer_line=answer_line+single_answer.values()[0]+","
                official_answer_line=official_answer_line+official_answers[single_answer.keys()[0]]+","
            #写学生答案
            if count==1:
                f.write(configure.report_listening_conversation+str(count)+"\n"+answer_line[:-1]+"\n")
            else:
                if count==4:
                    f.write(configure.report_listening_conversation+str(2)+"\n"+answer_line[:-1]+"\n")
                else:
                    f.write(configure.report_listening_lecture+str(count)+"\n"+answer_line[:-1]+"\n")

            #写标准答案
            f.write(official_answer_line[:-1]+"\n")



    @classmethod
    def generatReport(cls,userid,setid,mode):
        """
        生成学生报告
        Args:
            userid:学生id
            setid:哪一套题，例如20170603
            mode:什么模式

        """

        #首先判断学生是否有这套题
        questions=studentInfoDAO.getQuestionSetOfSingleStudent(userid)
        #如果学生有这套题
        if str(setid) in questions:
            result=answerDAO.queryAnswerForTPOSet(userid,setid,mode)
            print result
            #如果学生没做这套题
            if result==None:
                return configure.FAIL_CODE
            #如果学生做了这套题
            else:
                #获取标准答案
                official_answers=answerDAO.queryAnswerForTPOSet(configure.answer_officialid,setid,configure.answer_officialmode)
                print official_answers
                official_answers_sorted=sortDict(official_answers)

                #进行对比
                reading_answers=[]#存储阅读题的答案
                listening_answers=[]#存储听力题的答案

                #首先取听力部分

                count=0
                single_reading_answers={}
                single_listening_answer={}
                for official_answer in official_answers_sorted:
                    k=official_answer.keys()[0]
                    if "R" in k:
                        #
                        if k in result.keys():
                            single_reading_answers[k]=result[k]#获取学生答案
                        else:
                            single_reading_answers[k]=" "
                        

                        question=selection_questionDAO.getSelectionQuestion(setid,k)
                        #如果题号需要换了，就加入然后晴空
                        if question[configure.isLast]==1:
                            reading_answers.append(single_reading_answers)
                            single_reading_answers={}

                    #处理听力部分
                    if "L" in k:
                        if k in result.keys():
                            single_listening_answer[k]=result[k]
                        else:
                            single_listening_answer[k]=" "
                        question=selection_questionDAO.getSelectionQuestion(setid,k)
                        #如果题号需要换了，就加入然后清空
                        if question[configure.isLast]==1:
                            listening_answers.append(single_listening_answer)
                            single_listening_answer={}

                #进行排序，并输出
                print reading_answers
                print listening_answers
                cls.writeReport(reading_answers,listening_answers,official_answers,'/Users/apple/Code/report')

                #首先处理听力部分
                # for single_reading_answers in listening_answers:
        #如果学生没有这套题
        else:
            return configure.FAIL_CODE

if __name__ == '__main__':
    official_answer={"L18" : "C", "L19" : "BD", "L14" : "B", "L15" : "C", "L16" : "D", "L17" : "D", "L10" : "ACE", "L11" : "B", "L12" : "C", "L13" : "A", "R42" : "BDE", "R16" : "C", "R17" : "D", "R14" : "BEF", "R15" : "C", "R12" : "B", "R13" : "C", "R10" : "A", "R11" : "A", "R40" : "B", "R18" : "C", "R19" : "B", "L21" : "B", "L20" : "B", "L23" : "C", "L22" : "C", "L25" : "AB", "L24" : "D", "L27" : "C", "L26" : "C", "R34" : "C", "R35" : "D", "R36" : "A", "R37" : "B", "R30" : "D", "R31" : "C", "R32" : "C", "R33" : "C", "R4" : "A", "R5" : "C", "R6" : "D", "R7" : "C", "R39" : "B", "R1" : "B", "R2" : "B", "R3" : "B", "R28" : "ADE", "R8" : "B", "R9" : "B", "L6" : "B", "L29" : "BDE", "L4" : "B", "L5" : "C", "L2" : "C", "L3" : "A", "L1" : "D", "L8" : "D", "L9" : "C", "R24" : "D", "L30" : "B", "L7" : "A", "L32" : "C", "userid" : -1, "L28" : "B", "R38" : "A", "L34" : "D", "R41" : "D", "L33" : "D", "R29" : "A", "L31" : "A", "R27" : "A", "R26" : "A", "R25" : "B", "R23" : "D", "R22" : "A", "R21" : "C", "R20" : "D" }
    reading_test=[{'R1':'C','R12':"A",'R2':'D','R14':'ABC'},{'R15':'B','R27':"C",'R16':'D','R28':'ABC'},{'R29':'B','R41':"C",'R30':'D','R42':'ABC'}]
    listening_test=reading_test
    listening_test.extend(reading_test)
    # report_generator.writeReport(reading_test,listening_test,official_answer,'/Users/apple/Code/report')
    report_generator.generatReport(1,20170603,configure.answer_practicemode)

