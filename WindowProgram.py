# -*- coding: utf-8 -*-

import threading
import time


class WindowProgram(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.programs = None

    def setPrograms(self, programs):
        self.programs = programs
        self.server = programs['server']

    def run(self):
        while True:
            self.server.sendMessageForType(2, 'requestinfo')
            print('창문 정보 전송 요청')
            time.sleep(300)

    def updateWindowsData(self, name, msg):
        # split_msg[2] 열림/닫힘, split_msg[3] 온도, split_msg[4] 습도, split_msg[5] 강우량, split_msg[6] 먼지
        self.db.updateQuery(
            'insert into `window` values((select id from client where name = %s), %s, %s, %s, %s, '
            '%s) on duplicate key update `status` = %s, temp = %s, humi = %s, rain = %s, dust = %s',
            (name, msg[2], msg[3], msg[4], msg[5], msg[6], msg[2], msg[3],
             msg[4], msg[5], msg[6]))

    def openWindow(self, name):
        self.server.getUserClient()
        client = self.server.getUserClient(name)
        if client is None:
            return None
        self.server.sendMessage(client, 'openwindow')
        self.db.updateQuery('update window set status = true where name = %s', (name,))

    def closeWindow(self, name):
        client = self.server.getUserClient(name)
        if client is None:
            return None
        self.server.sendMessage(client, 'closewindow')
        self.db.updateQuery('update window set status = false where name = %s', (name,))
