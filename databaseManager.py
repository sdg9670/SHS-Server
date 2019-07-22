# -*- coding: utf-8 -*-
import pymysql


class DatabaseManager():
    def __init__(self, hosts, users, passwords, dbs):
        self.conn = pymysql.connect(host=hosts,
                                    user=users,
                                    password=passwords,
                                    db=dbs,
                                    cursorclass=pymysql.cursors.DictCursor
                                    )

    def dbClose(self):
        self.conn.close()

    def updateQuery(self, content, value):
        id = 0
        with self.conn.cursor() as cursor:
            cursor.execute(content, value)
            id = cursor.lastrowid
            self.conn.commit()
        return id


    def executeQuery2(self, content):
        with self.conn.cursor() as cursor:
            cursor.execute(content)
            return cursor.fetchall()

    def executeQuery(self, content, value):
        with self.conn.cursor() as cursor:
            cursor.execute(content, value)

            return cursor.fetchall()

    def executeOneQuery(self, content, value):
        with self.conn.cursor() as cursor:
            cursor.execute(content, value)
            return cursor.fetchone()
