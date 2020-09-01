# -*- coding: utf-8 -*-
"""



"""
import pymysql
def addaQuestionRecord(owner_id,owner_reputation,view_count,answer_count,score,question_id,title):
    #print(owner_id,owner_reputation,view_count,answer_count,score,question_id,title)
    db = pymysql.connect("localhost","root","123456","codereview" )
    cursor = db.cursor()    
    sql="INSERT INTO QUESTIONS_SET(OWNER_ID,OWNER_REPUTATION,VIEW_COUNT,\
                                ANSWER_COUNT,SCORE,QUESTION_ID,TITLE)\
                                VALUES('%d','%d','%d','%d','%d','%d','%s')"%\
                                (owner_id,owner_reputation,view_count,answer_count,score,question_id,title)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print("database error %s"%e)
        db.rollback()
    db.close()

def addaAnswerRecord(owner_id,owner_reputation,view_count,answer_count,score,question_id,title):
    sql="INSERT INTO QUESTIONS(OWNER_ID,OWNER_REPUTATION,VIEW_COUNT,\
                                ANSWER_COUNT,SCORE,QUESTION_ID,TITLE)\
                                VALUES('%d','%d','%d','%d','%d','%d','%s',)"%\
                                (owner_id,owner_reputation,view_count,answer_count,score,question_id,title)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    
def resetVis():
    """网络连接错误时重置数据库"""
    db = pymysql.connect("localhost","root","123456","codereview" )
    cursor = db.cursor()    
    for i in range(0,20000):
        sql="select * from questions_set where id=%d and answer_count>0;"%(i)
        try:
            if cursor.execute(sql)==0:
                continue
        except Exception as e:
            print("database error",e)
        else:
            res=cursor.fetchone()
            question_id=res[6]  # 4是answer_count
            sql="select count(*) from answers_set where question_id=%d;"%(res[6])
            try:
                cursor.execute(sql)
            except Exception as e:
                print("database error",e)
            else:
                if cursor.fetchone()[0]<res[4]:
                    sql="update questions_set set vis=0 where id=%d and vis=1;"%(i)
                    print("set",i)
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except Exception as e:
                        print("database error",e)
                        db.rollback()
    db.close()                
        
            


