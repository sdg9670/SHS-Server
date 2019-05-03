# -*- coding: utf-8 -*-

class AlarmProgram():
    def __init__(self, programs):
        self.programs = programs
        self.db = programs['db']
        self.alarms = []

    def addAlarm(self, date, time, week, content, username):
        self.db.updateSQL(
            'insert into alarm (date, time, week, content, userid) values (%s, %s, %s, %s, (select id from user where name = %s))'
            , (date, time, week, content, username))

    def updateAlarm(self, id, date, week, content):
        self.db.updateSQL('update alarm set date = %s, week = %s, content = %s where id=%s', (date, week, content, id))

    def removeAlarm(self, id):
        self.db.updateSQL('dalete from alarm where id=%s', (id,))

    def loadAlarm(self):
        result = self.db.excuteSQL('select * from alarm')
        for i in result:
            self.alarms.append(list(i))
