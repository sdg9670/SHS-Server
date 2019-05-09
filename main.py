# -*- coding: utf-8 -*-

import serverManager
import databaseManager
import windowProgram


# import alarmProgram

class Main:
    def __init__(self):
        self.programs = {}

    def start(self):
        try:
            self.programs['db'] = databaseManager.DatabaseManager('localhost', 'root', '!Dasom0129', 'shs')
            self.programs['server'] = serverManager.ServerManager('', 9670)
            self.programs['window'] = windowProgram.WindowProgram()

            self.programs['server'].setPrograms(self.programs)
            self.programs['server'].start()
            self.programs['window'].setPrograms(self.programs)
            self.programs['window'].start()

        except KeyboardInterrupt:
            print('[System] SHS 서버를 종료합니다.')
            self.programs['server'].serverClose()
            self.programs['db'].dbClose()


if __name__ == "__main__":
    main = Main()
    main.start()
