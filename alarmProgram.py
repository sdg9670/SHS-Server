# -*- coding: utf-8 -*-
from datetime import datetime
import json

class AlarmProgram():
    def __init__(self):

        self.programs = None
        self.server = None
        self.db = None
        self.alarms = {}

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
        data = self.db.executeQuery('select * from alarm where client_id = %s and datetime > now()', (clientid))
        dic = {}
        for index in data:
            dic[str(index[0])] = {'datetime':index[1].strftime('%Y/%m/%d %H:%M:%S'), 'content':index[2], 'clientid':index[3]}
        return json.dumps(dic)


    def getDatetime(self, dt):
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S+09:00')