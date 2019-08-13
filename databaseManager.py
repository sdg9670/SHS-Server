# -*- coding: utf-8 -*-
import pymysql
from sqlalchemy import pool

class DatabaseManager():
    def __init__(self, hosts, users, passwords, dbs):
       self.mypool = pool.QueuePool(lambda: pymysql.connect(host=hosts,
                                    user=users,
                                    password=passwords,
                                    db=dbs,
                                    cursorclass=pymysql.cursors.DictCursor
                                    ), pool_size=5, max_overflow=0)

    def dbClose(self):
        self.conn.close()

    def updateQuery(self, content, value):
        conn = self.mypool.connect()
        conn.autocommit(True)
        try:
            with conn.cursor() as cursor:
                cursor.execute(content, value)
                conn.commit()
        finally:
            conn.close()




    def executeQuery2(self, content):
        data = None
        conn = self.mypool.connect()
        conn.autocommit(True)
        try:
            with conn.cursor() as cursor:
                cursor.execute(content)
                data = cursor.fetchall()
        finally:
            conn.close()
        return data

    def executeQuery(self, content, value):
        data = None
        conn = self.mypool.connect()
        conn.autocommit(True)
        try:
            with conn.cursor() as cursor:
                cursor.execute(content, value)
                data = cursor.fetchall()
        finally:
            conn.close()
        return data

    def executeOneQuery(self, content, value):
        data = None
        conn = self.mypool.connect()
        conn.autocommit(True)
        try:
            with conn.cursor() as cursor:
                cursor.execute(content, value)
                data = cursor.fetchone()
        finally:
            conn.close()
        return data
