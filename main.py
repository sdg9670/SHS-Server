# -*- coding: utf-8 -*-

import serverManager
import databaseManager

# import alarmProgram

programs = {}

if __name__ == "__main__":

    try:
        db = databaseManager.DatabaseManager('localhost', 'root', '!Dasom0129', 'shs')
        programs['db'] = db;
        server = serverManager.ServerManager('', 9670, programs)
        programs['server'] = server;
        # alarm = alarmProgram.AlarmProgram(programs)
        # programs['alarm'] = db;
        server.start()
    except KeyboardInterrupt:
        print('[System] SHS 서버를 종료합니다.')
        server.serverClose()
        db.dbClose()
