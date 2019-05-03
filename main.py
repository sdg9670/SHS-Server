# -*- coding: utf-8 -*-

import serverManager
import databaseManager
import windowProgram

# import alarmProgram

programs = {}
class Main:
    def start(self):
        try:
            programs['db'] = databaseManager.DatabaseManager('localhost', 'root', '!Dasom0129', 'shs')
            programs['server'] = serverManager.ServerManager('', 9670)
            programs['window'] = windowProgram.WindowProgram()

            programs['server'].setPrograms(programs)
            programs['server'].start()
            programs['window'].setPrograms(programs)
            programs['window'].start()

        except KeyboardInterrupt:
            print('[System] SHS 서버를 종료합니다.')
            programs['server'].serverClose()
            programs['db'].dbClose()

if __name__ == "__main__":
    Main.start();
