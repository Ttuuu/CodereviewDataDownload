# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 17:35:58 2020

@author: ttu
"""


import pymysql
db = pymysql.connect("localhost","root","123456","codereview" )
cursor = db.cursor()    


sql="delete from answers_set where owner_reputation=0;"
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print("database error",e)
    db.rollback()
db.close()                

