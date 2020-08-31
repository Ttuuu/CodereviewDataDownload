# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 20:46:05 2020

@author: ttu
存数据库的时候有时候发生错误跳过了某些数据/请求超时但还是设置成了已访问
把收集到的answer个数不足question[answer_count]的问题重设为未访问
"""

import pymysql
db = pymysql.connect("localhost","root","123456","codereview" )
cursor = db.cursor()    

for i in range(0,20000):
    sql="select * from questions_set where id=%d and answer_count>0;"%(i)
    try:
        if cursor.execute(sql)==0:#根据id找到回答数大于0的问题
            continue
    except Exception as e:
        print("database error",e)
    else:
        res=cursor.fetchone()
        question_id=res[6]# 4 is answer_count
        sql="select count(*) from answers_set where question_id=%d;"%(res[6])#查找该问题在数据库中的回答个数
        try:
            cursor.execute(sql)
        except Exception as e:
            print("database error",e)
        else:
            if cursor.fetchone()[0]<res[4]:#回答数不足question[answer_count]
                sql="update questions_set set vis=0 where id=%d and vis=1;"%(i)#重设vis状态
                print("set",i)
                try:
                    cursor.execute(sql)
                    db.commit()
                except Exception as e:
                    print("database error",e)
                    db.rollback()
db.close()                
    
    