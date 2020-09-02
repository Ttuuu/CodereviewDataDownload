# -*- coding: utf-8 -*-
"""数据库相关操作"""
import pymysql

def addaQuestionRecord(owner_id,owner_reputation,view_count,answer_count,score,question_id,title):
    """插入一条问题记录
        参数
        -------
        owner_id : int            # 提问者id
        owner_reputation : int    # 提问者声誉
        view_count : int          # 问题访问次数
        answer_count : int        # 回答个数
        score : int               # 问题评分
        question_id : int         # 问题id
        title : str               # 问题标题

    """
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
    
def resetVis():
    """网络连接错误时重置数据库"""
    db = pymysql.connect("localhost","root","123456","codereview" )
    cursor = db.cursor()    
    for i in range(0,66639):
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
        
            


