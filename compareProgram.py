# -*- coding: utf-8 -*-

import threading
import time


class CompareProgram(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.programs = None
        self.server = None
        self.db = None

    def setPrograms(self, programs):
        self.programs = programs
        self.server = programs['server']
        self.db = programs['db']
        self.window = programs['window']
        self.curtain = programs['curtain']

    def run(self):
        while True:
            sensor = dict()
            for k in self.server.users:
                if self.server.users[k]['type'] == 5:
                    sensorResult = self.db.executeQuery('select * from sensor where id =%s', (k,))
                    for i in sensorResult:
                        sensor[self.server.users[k]['dong']] = dict()
                        sensor[self.server.users[k]['dong']][self.server.users[k]['ho']] = i

            print(sensor)

            for j in self.server.users:
                if self.server.users[j]['type'] == 2:
                    windowResult = self.db.executeQuery('select * from `window` where id = %s', (j,))
                    try:
                        se = sensor[self.server.users[j]['dong']][self.server.users[j]['ho']]
                    except Exception as e:
                        continue

                    if se['gas'] > 250:
                        self.window.openWindow(windowResult[0]['id'])

                    elif windowResult[0]['rain_over'] == 1:
                        if windowResult[0]['rain'] > 10:
                            if windowResult[0]['status'] == 1:
                                self.window.closeWindow(windowResult[0]['id'])

                    elif windowResult[0]['dust_over'] == 1:
                        if windowResult[0]['dust'] > windowResult[0]['dust_set']:
                            if windowResult[0]['status'] == 1:
                                self.window.closeWindow(windowResult[0]['id'])

                    elif windowResult[0]['temp_over'] == 1:
                        if se['temp'] > windowResult[0]['temp_set']:
                            if windowResult[0]['status'] == 0:
                                self.window.openWindow(windowResult[0]['id'])
                    elif windowResult[0]['temp_over'] == 2:
                        if se['temp'] < windowResult[0]['temp_set']:
                            if windowResult[0]['status'] == 1:
                                self.window.closeWindow(windowResult[0]['id'])
                    elif windowResult[0]['temp_over'] == 3:
                        if se['temp'] > windowResult[0]['temp']:
                            if windowResult[0]['status'] == 0:
                                self.window.openWindow(windowResult[0]['id'])
                    elif windowResult[0]['temp_over'] == 4:
                        if se['temp'] < windowResult[0]['temp']:
                            if windowResult[0]['status'] == 1:
                                self.window.closeWindow(windowResult[0]['id'])

                    elif windowResult[0]['humi_over'] == 1:
                        if se['humi'] > windowResult[0]['humi_set']:
                            if windowResult[0]['status'] == 0:
                                self.window.openWindow(windowResult[0]['id'])
                    elif windowResult[0]['humi_over'] == 2:
                        if se['humi'] < windowResult[0]['humi_set']:
                            if windowResult[0]['status'] == 1:
                                self.window.closeWindow(windowResult[0]['id'])
                    elif windowResult[0]['humi_over'] == 3:
                        if se['humi'] > windowResult[0]['humi']:
                            if windowResult[0]['status'] == 0:
                                self.window.openWindow(windowResult[0]['id'])
                    elif windowResult[0]['humi_over'] == 4:
                        if se['humi'] < windowResult[0]['humi']:
                            if windowResult[0]['status'] == 1:
                                self.window.closeWindow(windowResult[0]['id'])

            for m in self.server.users:
                if self.server.users[m]['type'] == 3:
                    curtainResult = self.db.executeQuery('select * from `curtain` where id = %s', (m,))
                    if curtainResult[0]['lux_over'] == 1:
                        if curtainResult[0]['lux'] > curtainResult[0]['lux_set']:
                            if curtainResult[0]['status'] == 0:
                                print("커튼 염 " + str(curtainResult[0]['lux']) + " " + str(curtainResult[0]['lux_set']))
                                self.curtain.openCurtain(curtainResult[0]['id'])
                    elif curtainResult[0]['lux_over'] == 2:
                        if curtainResult[0]['lux'] < curtainResult[0]['lux_set']:
                            if curtainResult[0]['status'] == 1:
                                print("커튼 닫음 " + str(curtainResult[0]['lux']) + " " + str(curtainResult[0]['lux_set']))
                                self.curtain.closeCurtain(curtainResult[0]['id'])
            time.sleep(15)