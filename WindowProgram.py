# -*- coding: utf-8 -*-

import threading
import time


class WindowProgram(threading.Thread):
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
            print('창문 정보 전송 요청')
            self.server.sendMessageForType(2, 'requestinfo')
            time.sleep(30)

    def updateWindowsData(self, name, msg):
        # split_msg[2] 열림/닫힘, split_msg[3] 온도, split_msg[4] 습도, split_msg[5] 강우량, split_msg[6] 먼지
        self.db.updateQuery(
            'insert into `window` (id, status, temp, humi, rain, dust) values((select id from client where name = %s), %s, %s, %s, %s, '
            '%s) on duplicate key update `status` = %s, temp = %s, humi = %s, rain = %s, dust = %s',
            (name, msg[2], msg[3], msg[4], msg[5], msg[6], msg[2], msg[3],
             msg[4], msg[5], msg[6]))

    def openWindow(self, key):
        self.server.sendMessage(self.server.users[key]['client'], 'openwindow')
        self.db.updateQuery('update `window` set `status` = true where id = %s', (key,))

    def closeWindow(self, key):
        self.server.sendMessage(self.server.users[key]['client'], 'closewindow')
        self.db.updateQuery('update `window` set `status` = false where id = %s', (key,))
