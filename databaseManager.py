# -*- coding: utf-8 -*-
import pymysql.cursors
 
class DatabaseManager():
    def __init__(self, hosts, users, passwords, dbs):
        self.conn = pymysql.connect(host=hosts,
            user=users,
            password=passwords,
            db = dbs)
    def dbClose(self):
        self.conn.close()
        
    def updateQuery(self, content, value):
        with self.conn.cursor() as cursor:
            cursor.execute(content, value)
            self.conn.commit()
          
    def executeQuery(self, content, value):
        with self.conn.cursor() as cursor:
            cursor.execute(content, value)
            return cursor.fetchall()
    def executeOneQuery(self, content, value):
        with self.conn.cursor() as cursor:
            cursor.execute(content, value)
            return cursor.fetchone()
            