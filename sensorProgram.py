# -*- coding: utf-8 -*-

import threading
import time


class SensorProgram(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.programs = None
        self.server = None
        self.db = None

    def setPrograms(self, programs):
        self.programs = programs
        self.server = programs['server']
        self.db = programs['db']

    def run(self):
        while True:
            print('센서 정보 전송 요청')
            self.server.sendMessageForType(5, 'requestinfo')
            time.sleep(10)

    def updateSensorData(self, name, msg):
        # split_msg[2] 열림/닫힘, split_msg[3] 온도, split_msg[4] 습도, split_msg[5] 강우량, split_msg[6] 먼지
        self.db.updateQuery(
            'insert into `curtain` (id, `status`, lux) values((select id from client where name = %s), %s, %s)'+
            ' on duplicate key update `status` = %s, lux = %s',
            (name, msg[2], msg[3], msg[2], msg[3]))

    def openSensor(self, key):
        self.server.sendMessage(self.server.users[key]['client'], 'opencurtain')
        self.db.updateQuery('update `curtain` set `status` = true where id = %s', (key,))

    def closeSensor(self, key):
        self.server.sendMessage(self.server.users[key]['client'], 'closecurtain')
        self.db.updateQuery('update `curtain` set `status` = false where id = %s', (key,))
