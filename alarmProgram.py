# -*- coding: utf-8 -*-
from datetime import datetime
import json

class AlarmProgram():
    def __init__(self):

        self.programs = None
        self.server = None
        self.db = None
        self.alarms = {}

    def json_default(self, value):
        if isinstance(value, datetime):
            return value.__str__()

    def setPrograms(self, programs):
        self.programs = programs
        self.server = programs['server']
        self.db = programs['db']

    def addAlarm2(self, datetime, clientid):
        self.db.updateQuery(
            'insert into alarm (datetime, client_id) values (%s, %s)'
            , (datetime, clientid))

    def addAlarm(self, datetime, content, clientid):
        self.db.updateQuery(
            'insert into alarm (datetime, content, client_id) values (%s, %s, %s)'
            , (datetime, content, clientid))

    def updateAlarm(self, datetime1, datetime2, clientid):
        self.db.updateQuery('update alarm set datetime = %s where datetime=%s and client_id = %s', (datetime2, datetime1, clientid))

    def removeAlarm(self, datetime, clientid):
        self.db.updateQuery('delete from alarm where datetime=%s and client_id = %s', (datetime, clientid))

    def loadAlarm(self, clientid):
        data = self.db.executeQuery('select * from alarm where client_id = %s and datetime > now()', (clientid,))
        dic = {}
        for index in data:
            print(str(list(index.values())[0]))
            dic[list(index.values())[0]] = index
        return json.dumps(dic, default=self.json_default)

    def getDatetime(self, dt):
        print(dt)
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S+09:00')

    def dateToString(self, dt):
        return self.getDatetime(dt).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')

    def contentAnal(self, string):
        a = ''
        if string.find('으라고', len(string) - 3) > 0:
            a = string.split('으라고')[0] + '기'
        elif string.find('라고', len(string) - 2) > 0:
            a = string.split('라고')[0] + '기'
        elif string.find('게', len(string) - 1) > 0:
            a = string.split('게')[0] + '기'
        elif string.find('로', len(string) - 1) > 0:
            a = string.split('로')[0]
        return a