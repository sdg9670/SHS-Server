# -*- coding: utf-8 -*-

import serverManager
import databaseManager
import windowProgram
import alarmProgram
import curtainProgram
import sensorProgram
import compareProgram
import os

# import alarmProgram

class Main:
    def __init__(self):
        self.programs = {}
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialog.json"

    def start(self):
        try:
            self.programs['db'] = databaseManager.DatabaseManager('localhost', 'root', '!Dasom0129', 'shs')
            self.programs['server'] = serverManager.ServerManager('', 9670)
            self.programs['window'] = windowProgram.WindowProgram()
            self.programs['curtain'] = curtainProgram.CurtainProgram()
            self.programs['alarm'] = alarmProgram.AlarmProgram()
            self.programs['sensor'] = sensorProgram.SensorProgram()
            self.programs['compare'] = compareProgram.CompareProgram()

            self.programs['server'].setPrograms(self.programs)
            self.programs['server'].start()
            self.programs['window'].setPrograms(self.programs)
            self.programs['window'].start()
            self.programs['curtain'].setPrograms(self.programs)
            self.programs['curtain'].start()
            self.programs['sensor'].setPrograms(self.programs)
            self.programs['sensor'].start()
            self.programs['alarm'].setPrograms(self.programs)
            self.programs['compare'].setPrograms(self.programs)
            self.programs['compare'].start()

        except KeyboardInterrupt:
            print('[System] SHS 서버를 종료합니다.')
            self.programs['server'].serverClose()
            self.programs['db'].dbClose()


if __name__ == "__main__":
    main = Main()
    main.start()
