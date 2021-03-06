# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

import sys
sys.path.append('../configure/')
sys.path.append('../model/')
sys.path.append('../dao/')
reload(sys)
sys.setdefaultencoding('utf-8')
import configure
from studentInfoDAO import studentInfoDAO
from answerDAO import answerDAO
from selection_questionDAO import selection_questionDAO
from dict_op import sortDict
from report_doc_generator import write_doc

class report_generator(object):
    """用于生成客观题报告"""

    @classmethod
    def calculateScoreForListening(cls,listening_answers):
        """
        计算听力部分的最终得分
        Args:
            listening_answers:听力题答案
        """
        score=0
        scaled_score=0
        for single_listening_answers in listening_answers:
            for single_answer in single_listening_answers:
                
                student_answer=str(sorted(single_answer.keys()[0]))
                official_answer=str(sorted(single_answer[single_answer.keys()[0]]))
                #如果回答正确
                if cmp(student_answer,official_answer)==0:
                    score+=1
                #如果回答错误，就不管了
        #进行转换
        if score<=4:
            scaled_score=0
        elif score==5:
            scaled_score=1
        elif score<=7:
            scaled_score=2
        elif score<=9:
            scaled_score=3
        elif score==10:
            scaled_score=4
        elif score<=12:
            scaled_score=5
        elif score==13:
            scaled_score=6
        elif score==14:
            scaled_score=7
        elif score==15:
            scaled_score=8
        elif score==16:
            scaled_score=9
        elif score==17:
            scaled_score=10
        elif score==18:
            scaled_score=11
        elif score==19:
            scaled_score=13
        elif score==20:
            scaled_score=14
        elif score==21:
            scaled_score=15
        elif score==22:
            scaled_score=17
        elif score==23:
            scaled_score=18
        elif score==24:
            scaled_score=19
        elif score==25:
            scaled_score=21
        elif score==26:
            scaled_score=22
        elif score==27:
            scaled_score=23
        elif score==28:
            scaled_score=25
        elif score==29:
            scaled_score=26
        elif score==30:
            scaled_score=27
        elif score==31:
            scaled_score=28
        elif score==32:
            scaled_score=29
        else:
            scaled_score=30
        return scaled_score


    @classmethod
    def calculateScoreForReading(cls,reading_answers):
        """
        计算听力部分的最终得分
        Args:
            reading_answers:阅读题答案
        """
        score=0
        scaled_score=0
        for single_reading_answers in reading_answers:
            for single_answer in single_reading_answers:
                student_answer=single_answer.keys()[0]
                official_answer=single_answer[student_answer]
                #如果回答正确
                if cmp(student_answer,official_answer)==0:
                    #如果是单选题，就加一分
                    if len(official_answer)==1:
                        score+=1
                    #如果是多选题
                    else:
                        score+=2
                #如果回答错误
                else:
                    #如果是单选题，就不加分
                    #如果是多选题，错一个加一分，错两个以上，就不加分
                    if len(official_answer)>1:
                        false_count=0
                        #统计错误数
                        for answer in official_answer:
                            if answer not in student_answer:
                                false_count+=1
                        #计算分数
                        if false_count==0:
                            score+=2
                        elif false_count==1:
                            score+=1
        #score求出来，现在换算分数
        if score<=9:
            scaled_score=0
        elif score<=11:
            scaled_score=1
        elif score<=13:
            scaled_score=2
        elif score==14:
            scaled_score=3
        elif score==15:
            scaled_score=4
        elif score==16:
            scaled_score=5
        elif score==17:
            scaled_score=7
        elif score==18:
            scaled_score=8
        elif score==19:
            scaled_score=9
        elif score==20:
            scaled_score=10
        elif score==21:
            scaled_score=11
        elif score==22:
            scaled_score=13
        elif score==23:
            scaled_score=14
        elif score==24:
            scaled_score=15
        elif score==25:
            scaled_score=16
        elif score==26:
            scaled_score=17
        elif score==27:
            scaled_score=18
        elif score==28:
            scaled_score=19
        elif score==29:
            scaled_score=20
        elif score==30:
            scaled_score=21
        elif score==31:
            scaled_score=22
        elif score==32:
            scaled_score=23
        elif score==33:
            scaled_score=24
        elif score<=35:
            scaled_score=25
        elif score==36:
            scaled_score=26
        elif score<=38:
            scaled_score=27
        elif score<=40:
            scaled_score=28
        elif score<=44:
            scaled_score=29
        else:
            scaled_score=30
        return scaled_score
                    

        pass       

    

    @classmethod
    def writeReport(cls,reading_answers,listening_answers,reading_score,listening_score,report_path):
        """
        生成报告正文，包括阅读和听力
        Args:
            reading_answers:阅读题答案[[{'A':'A'},{'B':'B'}][]]
            listening_answers:听力题答案
            report_path:报告的路径
            official_answers:标准答案
        """
        f=open(report_path,'w')
        count=0


        #先写阅读题答案
        f.write("阅读部分得分:"+str(reading_score)+"\n")
        for single_reading_answers in reading_answers:
            #每一套阅读题
            count+=1
            #构造一行答案
            answer_line=""
            official_answer_line=""
            for single_answer in single_reading_answers:
                student_answer=single_answer.keys()[0]
                official_answer=single_answer.get(student_answer)
                answer_line=answer_line+student_answer+","
                official_answer_line=official_answer_line+official_answer+","
            #写学生答案
            f.write(configure.report_reading+str(count)+"\n"+answer_line[:-1]+"\n")
            #写标准答案
            f.write(official_answer_line[:-1]+"\n")

        #写听力题答案
        f.write("\n")
        f.write("听力部分得分:"+str(listening_score)+"\n")
        count=0
        for single_listening_answers in listening_answers:
            count+=1
            #构造一行答案
            answer_line=""
            official_answer_line=""
            for single_answer in single_listening_answers:
                student_answer=single_answer.keys()[0]
                official_answer=single_answer.get(student_answer)
                answer_line=answer_line+student_answer+","
                official_answer_line=official_answer_line+official_answer+","
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
        f.close()



    @classmethod
    def generatReport(cls,userid,setid,mode,path):
        """
        生成学生报告
        Args:
            userid:学生id
            setid:哪一套题，例如20170603
            mode:什么模式
            path:报告存到哪里

        """
        #先获取对比答案
        answers=answerDAO.getAnswerInComparison(setid,userid,mode)
        #如果获取到的对比答案是空，就不进行处理
        if answers==[]:
            return configure.FAIL_CODE
        #如果不是空，就进行处理

        #提取答案
        reading_answers=answers[0]
        listening_answers=answers[1]
        #计算阅读分数
        reading_score=cls.calculateScoreForReading(reading_answers)
        #计算听力分数
        listening_score=cls.calculateScoreForListening(listening_answers)
        #写报告
        # cls.writeReport(reading_answers,listening_answers,reading_score,listening_score,path)
        write_doc(setid,reading_answers,listening_answers,reading_score,listening_score,path)

        return configure.SUCCESS_CODE

if __name__ == '__main__':
    official_answer={"L18" : "C", "L19" : "BD", "L14" : "B", "L15" : "C", "L16" : "D", "L17" : "D", "L10" : "ACE", "L11" : "B", "L12" : "C", "L13" : "A", "R42" : "BDE", "R16" : "C", "R17" : "D", "R14" : "BEF", "R15" : "C", "R12" : "B", "R13" : "C", "R10" : "A", "R11" : "A", "R40" : "B", "R18" : "C", "R19" : "B", "L21" : "B", "L20" : "B", "L23" : "C", "L22" : "C", "L25" : "AB", "L24" : "D", "L27" : "C", "L26" : "C", "R34" : "C", "R35" : "D", "R36" : "A", "R37" : "B", "R30" : "D", "R31" : "C", "R32" : "C", "R33" : "C", "R4" : "A", "R5" : "C", "R6" : "D", "R7" : "C", "R39" : "B", "R1" : "B", "R2" : "B", "R3" : "B", "R28" : "ADE", "R8" : "B", "R9" : "B", "L6" : "B", "L29" : "BDE", "L4" : "B", "L5" : "C", "L2" : "C", "L3" : "A", "L1" : "D", "L8" : "D", "L9" : "C", "R24" : "D", "L30" : "B", "L7" : "A", "L32" : "C", "userid" : -1, "L28" : "B", "R38" : "A", "L34" : "D", "R41" : "D", "L33" : "D", "R29" : "A", "L31" : "A", "R27" : "A", "R26" : "A", "R25" : "B", "R23" : "D", "R22" : "A", "R21" : "C", "R20" : "D" }
    reading_test=[{'R1':'C','R12':"A",'R2':'D','R14':'ABC'},{'R15':'B','R27':"C",'R16':'D','R28':'ABC'},{'R29':'B','R41':"C",'R30':'D','R42':'ABC'}]
    listening_test=reading_test
    listening_test.extend(reading_test)
    # report_generator.writeReport(reading_test,listening_test,official_answer,'/Users/apple/Code/report')
    report_generator.generatReport(1,20170603,configure.answer_exammode,"./report.docx")

