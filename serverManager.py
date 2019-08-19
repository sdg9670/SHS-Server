# -*- coding: utf-8 -*-
import json
import socket
import threading
from datetime import datetime

import naturalLanguage
import wikiCrawler
from crawler.crawler import crawl
from crawler.weatherToday import weatherToday
from crawler.weatherTomorrow import weatherTomorrow
from crawler.weatherAfterTommorow import weatherAfterTommorow
import requests

lock = threading.Lock()


class ServerManager(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.users = {}
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.programs = None
        self.db = None
        self.window = None

    def setPrograms(self, programs):
        self.db = programs['db']
        self.window = programs['window']
        self.alarm = programs['alarm']
        self.curtain = programs['curtain']
        self.sensor = programs['sensor']

    def run(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.listenToClient, args=(client, address)).start()
            threading.Thread()

    def listenToClient(self, client, address):
        size = 1024
        recv = client.recv(size).decode('utf-8')

        if '\tandroid\t' in recv:
            data = recv.split('\tandroid\t')
            key = int(data[0])
            if not self.addUser(key, client, address):
                client.close()
                return
            self.searchProgram(client, 'android\t' + data[1])
            self.removeUser(key)
            client.close()
            return

        key = int(recv)
        print(key)
        if not self.addUser(key, client, address):
            client.close()
            return

        print('[System] %s [%d] %s 접속함' % (self.users[key]['address'], self.users[key]['id'], self.users[key]['name']))
        print('[System] 서버 클라이언트 수 [%d]' % len(self.users))

        while True:
            try:
                data = client.recv(size)
                if data:
                    self.searchProgram(client, str(data.decode('utf-8')))
                else:
                   raise ValueError('클라이언트 종료')
            except Exception as e:
                print('[System] %s %s 종료함' % (self.users[key]['address'], self.users[key]['address']))
                self.removeUser(key)
                client.close()
                print('[System] 서버 클라이언트 수 [%d]' % len(self.users))
                print('[System] Error: %s' % e)
                break
        '''
        #try:
            data = client.recv(size)
            if data:
                self.searchProgram(client, str(data.decode('utf-8')))
            else:
                raise ValueError('클라이언트 종료')
        #except Exception as e:
                print('[System] %s %s 종료함' % (self.users[key]['address'], self.users[key]['address']))
                self.removeUser(key)
                client.close()
                print('[System] 서버 클라이언트 수 [%d]' % len(self.users))
                print('[System] Error: %s' % e)
                break
        '''

    def getSocket(self):
        return self.sock

    def serverClose(self):
        self.sock.close()

    def sendMessage(self, client, msg):
        print('전송: ' + msg)
        client.send(('server\t' + msg).encode('utf-8'))

    def addUser(self, key, client, address):
        if key in self.users:
            print('[Server] %d 이미 접속된 클라이언트\n' % key)
            return False
        result = self.db.executeQuery('select * from client where id = %s', (key,))
        if result is None:
            print('[Server] $s 등록되지 않은 클라이언트\n' % key)
            return False
        print(result)
        key = list(result[0].values())[0]
        lock.acquire()
        self.users[list(result[0].values())[0]] = result[0]
        self.users[key]['client'] = client
        self.users[key]['address'] = address
        print('접속', self.users[key])
        lock.release()
        return True

    def removeUser(self, key):
        if key not in self.users:
            return
        lock.acquire()
        del self.users[key]
        lock.release()

    def searchProgram(self, client, msg):
        print(msg)
        split_msg = msg.split("\t")
        if split_msg[0] == "speaker":
            if split_msg[1] == "nal":
                # split_msg[2] session, split_msg[3] content
                nal = naturalLanguage.NaturalLanguage('newagent-855b9', split_msg[2], split_msg[3], 'ko-KR')
                func = nal.getData()
                print(nal.getParameter())
                print(nal.getText())
                print(nal.getData())
                if func[2] == 'A':
                    stat = self.runProgram(client, func[0], func[1], func[3], nal.getParameter());
                    if stat is not None :
                        self.sendMessage(client, 'msg\t' + stat)
                    else:
                        self.sendMessage(client, 'msg\ta\t' + nal.getText())
                elif func[2] == 'Q':
                    self.sendMessage(client, 'msg\tq\t' + nal.getText())
            elif split_msg[1] == "getalarm":
                alarmlist = self.alarm.loadAlarm(self.getUsersKey(client))
                if alarmlist is not None:
                    self.sendMessage(client, 'getalarm\t' + alarmlist)
            elif split_msg[1] == "help":
                data = {'title': '네이봇 [도움요청]', 'message': str(self.users[self.getUsersKey(client)]['dong']) + '동 ' +  str(self.users[self.getUsersKey(client)]['ho']) + '호에서 긴급 도움을 요청하였습니다.', 'dong': self.users[self.getUsersKey(client)]['dong']}
                requests.post('http://simddong.ga:5000/sendfcm_dong', data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
                for k in self.users:
                    if self.users[k]['type'] == 0:
                        if self.users[k]['dong'] == self.users[self.getUsersKey(client)]['dong']:
                            if self.users[k]['ho'] != self.users[self.getUsersKey(client)]['ho']:
                                self.sendMessage(self.users[k]['client'], 'msg\ta\t'+str(self.users[self.getUsersKey(client)]['dong'])+'동 '+str(self.users[self.getUsersKey(client)]['ho'])+'호에서 긴급 도움을 요청하였습니다.')
                self.sendMessage(client, 'msg\ta\t도움 요청이 전송되었습니다.')
        elif split_msg[0] == "sensor":
            if split_msg[1] == "inputsql":
                # split_msg[2] 온도, split_msg[3] 습도, split_msg[4]가스
                self.db.updateQuery(
                    'update `sensor` set `temp` = %s, `humi` = %s, `gas` = %s where id = %s',
                    (split_msg[2], split_msg[3], split_msg[4], self.getUsersKey(client)))

        elif split_msg[0] == "window":
            if split_msg[1] == "inputsql":
                print(split_msg[2])
                #상태 온도 습도 강수량 미세먼지
                if split_msg[2] == "false":
                    split_msg[2] = False
                elif split_msg[2] == "true":
                    split_msg[2] = True
                print(split_msg[2])
                self.db.updateQuery(
                    'update `window` set `status` = %s, temp = %s, humi = %s, rain = %s, dust = %s where id = %s',
                    (split_msg[2], split_msg[3], split_msg[4], split_msg[5], split_msg[6], self.getUsersKey(client)))

        elif split_msg[0] == "curtain":
            if split_msg[1] == "inputsql":
                # split_msg[2] 열림/닫힘, split_msg[3] 조도
                if split_msg[2] == "false":
                    split_msg[2] = False
                elif split_msg[2] == "true":
                    split_msg[2] = True
                self.db.updateQuery(
                    'update `curtain` set `status` = %s, lux = %s where id = %s',
                    (split_msg[2], split_msg[3], self.getUsersKey(client)))

        elif split_msg[0] == "doorlock":
            if split_msg[1] == "enroll":
                key = self.getUsersKey(client)
                self.db.updateQuery(
                    'insert into fingerprint (finger, dong, ho) values(%s, %s, %s) on duplicate key '
                    'update finger = %s, dong = %s, ho = %s',
                    (split_msg[2], self.users[key]['dong'], self.users[key]['ho'], split_msg[2], self.users[key]['dong'], self.users[key]['ho']))
            elif split_msg[1] == "image":
                data = {'title': '네이봇 [도어락]', 'message': split_msg[3] + '에 도어락 틀림이 감지되었습니다.', 'ho': self.users[self.getUsersKey(client)]['ho'], 'dong': self.users[self.getUsersKey(client)]['dong']}
                requests.post('http://simddong.ga:5000/sendfcm_ho_dong', data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
                key = self.getUsersKey(client)
                self.db.updateQuery(
                    'insert into doorlock_image (path, upload_time, state, dong, ho) values(%s, %s, %s, %s, %s)',
                    (split_msg[2], split_msg[3], split_msg[4], self.users[key]['dong'], self.users[key]['ho']))

        elif split_msg[0] == "android":
            if split_msg[1] == "command":
                # split_msg[2] session, split_msg[3] content
                print(split_msg[2])
                nal = naturalLanguage.NaturalLanguage('newagent-855b9', split_msg[2], split_msg[3], 'ko-KR')
                func = nal.getData()
                print(nal.getParameter())
                print(nal.getText())
                print(nal.getData())
                if func[2] == 'A':
                    stat = self.runProgram(client, func[0], func[1], func[3], nal.getParameter());
                    if stat is not None :
                        self.sendMessage(client, 'msg\t' + stat)
                    else:
                        self.sendMessage(client, 'msg\ta\t' + nal.getText())
                elif func[2] == 'Q':
                    self.sendMessage(client, 'msg\tq\t' + nal.getText())
            elif split_msg[1] == "help":
                data = {'title': '네이봇 [도움요청]', 'message': str(self.users[self.getUsersKey(client)]['dong']) + '동 ' +  str(self.users[self.getUsersKey(client)]['ho']) + '호에서 긴급 도움을 요청하였습니다.', 'dong': self.users[self.getUsersKey(client)]['dong']}
                requests.post('http://simddong.ga:5000/sendfcm_dong', data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
                for k in self.users:
                    if self.users[k]['type'] == 0:
                        if self.users[k]['dong'] == self.users[self.getUsersKey(client)]['dong']:
                            if self.users[k]['ho'] != self.users[self.getUsersKey(client)]['ho']:
                                self.sendMessage(self.users[k]['client'], 'msg\ta\t'+str(self.users[self.getUsersKey(client)]['dong'])+'동 '+str(self.users[self.getUsersKey(client)]['ho'])+'호에서 긴급 도움을 요청하였습니다.')
                self.sendMessage(client, 'msg\ta\t도움 요청이 전송되었습니다.')

    def runProgram(self, client, program, function, type, parameter):
        key = self.getUsersKey(client)
        if program == 1:
            if function == 1:
                if self.users[key]['type'] == 10:
                    return 'a\t핸드폰에서 알람 기능을 사용할 수 없습니다.'
                strs = ''
                if type == 1:
                    if isinstance(parameter['date-time'], dict):
                        self.alarm.addAlarm2(self.alarm.getDatetime(parameter['date-time']['startDateTime']), self.getUsersKey(client))
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']['startDateTime']) + '에 알람을 맞췄습니다.'
                        print(self.alarm.dateToString(parameter['date-time']['startDateTime']))
                    else:
                        self.alarm.addAlarm2(self.alarm.getDatetime(parameter['date-time']), self.getUsersKey(client))
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']) + '에 알람을 맞췄습니다.'
                        print(self.alarm.dateToString(parameter['date-time']))
                    self.sendMessage(client, 'getalarm\t' + self.alarm.loadAlarm(self.getUsersKey(client)))
                    return strs
                if type == 2:
                    if isinstance(parameter['date-time'], dict):
                        self.alarm.addAlarm(self.alarm.getDatetime(parameter['date-time']['startDateTime']), self.alarm.contentAnal(parameter['AlarmContent']), self.getUsersKey(client))
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']['startDateTime']) + '에 ' + self.alarm.contentAnal(parameter['AlarmContent']) + ' 알람을 맞췄습니다.'
                    else:
                        self.alarm.addAlarm(self.alarm.getDatetime(parameter['date-time']), self.alarm.contentAnal(parameter['AlarmContent']), self.getUsersKey(client))
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']) + '에 ' + self.alarm.contentAnal(parameter['AlarmContent']) + ' 알람을 맞췄습니다.'
                    self.sendMessage(client, 'getalarm\t' + self.alarm.loadAlarm(self.getUsersKey(client)))
                    return strs
            elif function == 2:
                if type == 1:
                    if isinstance(parameter['date-time'], dict):
                        self.alarm.removeAlarm(self.alarm.getDatetime(parameter['date-time']['startDateTime']), self.getUsersKey(client))
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']['startDateTime']) + ' 알람을 삭제하였습니다.'
                    else:
                        self.alarm.removeAlarm(self.alarm.getDatetime(parameter['date-time']), self.getUsersKey(client))
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']) + ' 알람을 삭제하였습니다.'
                    self.sendMessage(client, 'getalarm\t' + self.alarm.loadAlarm(self.getUsersKey(client)))
                    return strs
            elif function == 3:
                if type == 1:
                    time1 = None
                    time2 = None
                    if isinstance(parameter['date-time'], dict):
                        time1 = self.alarm.getDatetime(parameter['date-time']['startDateTime'])
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']['startDateTime']) + ' 알람을 '
                    else:
                        time1 = self.alarm.getDatetime(parameter['date-time'])
                        strs = 'a\t' + self.alarm.dateToString(parameter['date-time']) + ' 알람을 '
                    if isinstance(parameter['date-time1'], dict):
                        time2 = self.alarm.getDatetime(parameter['date-time1']['startDateTime'])
                        strs += self.alarm.dateToString(parameter['date-time1']['startDateTime']) + ' 로 수정하였습니다.'
                    else:
                        time2 = self.alarm.getDatetime(parameter['date-time1'])
                        strs += self.alarm.dateToString(parameter['date-time1']) + ' 로 수정하였습니다.'
                    self.alarm.updateAlarm(time1, time2, self.getUsersKey(client))
                    self.sendMessage(client, 'getalarm\t' + self.alarm.loadAlarm(self.getUsersKey(client)))
                    return strs


        elif program == 2:
            if function == 1:
                if type == 1:
                    #[2-1-A-1]
                    window = self.getInClient(parameter['WindowName'], 2, self.users[key]['ho'], self.users[key]['dong'])
                    if window is None:
                        return "a\t존재하지 않는 창문입니다."
                    self.window.openWindow(window)
            elif function == 2:
                if type == 1:
                    #[2-2-A-1]
                    window = self.getInClient(parameter['WindowName'], 2, self.users[key]['ho'], self.users[key]['dong'])
                    if window is None:
                        return "a\t존재하지 않는 창문입니다."
                    self.window.closeWindow(window)

        elif program == 3:
            if function == 1:
                if type == 1:
                    #[3-1-A-1]
                    curtain = self.getInClient(parameter['WindowName'], 3, self.users[key]['ho'], self.users[key]['dong'])

                    if curtain is None:
                        return "a\t존재하지 않는 커튼입니다."
                    print('커텐열기')
                    self.curtain.openCurtain(curtain)
            elif function == 2:
                if type == 1:
                    #[3-2-A-1]
                    curtain = self.getInClient(parameter['WindowName'], 3, self.users[key]['ho'], self.users[key]['dong'])

                    if curtain is None:
                        return "a\t존재하지 않는 커튼입니다."
                    print('커텐닫기')
                    self.curtain.closeCurtain(curtain)

        elif program == 4:
            if function == 1:
                if type == 1:
                    doorlock = self.getDoorlock(4, self.users[key]['ho'], self.users[key]['dong'])
                    if doorlock is None:
                        return "a\t도어락이 존재하지 않습니다."
                    self.sendMessage(self.users[doorlock]['client'], 'open')

            elif function == 2:
                if type == 1:
                    doorlock = self.getDoorlock(4, self.users[key]['ho'], self.users[key]['dong'])
                    if doorlock is None:
                        return "a\t도어락이 존재하지 않습니다."
                    self.sendMessage(self.users[doorlock]['client'], 'enroll')

        elif program == 6:
            if function == 1:
                if type == 1:
                    dtnow = datetime.now()
                    dt = datetime.strptime(parameter['date-time'], '%Y-%m-%dT%H:%M:%S+09:00')
                    dw = (dt.date() - dtnow.date()).days
                    ww = ['오늘', '내일', '모레']
                    if dw == 0:
                        weather = weatherToday(crawl(ww[dw] + '%20' + parameter['Location'] + '%20날씨'))
                        if weather is None:
                            return 'a\t알 수 없는 지역입니다.'
                        m = '오늘 ' + weather['날씨']['지역'] + ' 날씨는 ' + weather['날씨']['날씨'] + '. 현재온도는 ' + weather['날씨']['온도'].split('씨℃')[0] + ', 최저기온은 ' + weather['날씨']['최저기온'] + ', 최고기온은 ' + weather['날씨']['최고기온'] + ' 입니다. 체감온도는 ' + weather['날씨']['체감온도'] + ' 입니다.'
                        if self.users[key]['type'] == 10:
                            return 'a\t' + m
                        return 'weathertoday\t' + m + '\t' + str(weather)
                    elif dw == 1:
                        weather = weatherTomorrow(crawl(ww[dw] + '%20' + parameter['Location'] + '%20날씨'))
                        if weather is None:
                            return 'a\t알 수 없는 지역입니다.'
                        m = weather['날씨']['지역'] + '의 내일 오전 날씨는 ' + weather['날씨']['오전날씨'] + '이고 ' + weather['날씨']['오전온도'].split('씨℃')[0] + '입니다. ' + '오후 날씨는 ' + weather['날씨']['오후날씨'] + '이고 ' + weather['날씨']['오후온도'].split('씨℃')[0] + '입니다. '
                        if self.users[key]['type'] == 10:
                            return 'a\t' + m
                        return 'weathertommorow\t' + m + '\t' + str(weather)
                    elif dw == 2:
                        weather = weatherAfterTommorow(crawl(ww[dw] + '%20' + parameter['Location'] + '%20날씨'))
                        if weather is None:
                            return 'a\t알 수 없는 지역입니다.'
                        m = weather['날씨']['지역'] + '의 내일 모레의 오전 날씨는 ' + weather['날씨']['오전날씨'] + '이고 ' + weather['날씨']['오전온도'].split('씨℃')[0] + '입니다. ' + '오후 날씨는 ' + weather['날씨']['오후날씨'] + '이고 ' + weather['날씨']['오후온도'].split('씨℃')[0] + '입니다. '
                        if self.users[key]['type'] == 10:
                            return 'a\t' + m
                        return 'weatheraftertommorow\t' + m + '\t' + str(weather)
                    else:
                        return 'a\t' + '이 날의 날씨는 모르겠어요~'
                elif type == 2:
                        weather = weatherToday(crawl('오늘' + '%20' + parameter['Location'] + '%20날씨'))
                        if weather is None:
                            return 'a\t알 수 없는 지역입니다.'
                        m = '오늘 ' + weather['날씨']['지역'] + ' 날씨는 ' + weather['날씨']['날씨'] + '. 현재온도는 ' + weather['날씨']['온도'].split('씨℃')[0] + ', 최저기온은 ' + weather['날씨']['최저기온'] + ', 최고기온은 ' + weather['날씨']['최고기온'] + ' 입니다. 체감온도는 ' + weather['날씨']['체감온도'] + ' 입니다.'
                        if self.users[key]['type'] == 10:
                            return 'a\t' + m
                        return 'weathertoday\t' + m + '\t' + str(weather)

        elif program == 7:
            if function == 1:
                if type == 1:
                    wiki = wikiCrawler.WikiCrawler()
                    data = wiki.get(parameter['WikiName'])
                    if data is None:
                        return 'a\t제가 알고 있는 단어가 아니에요.'
                    return 'a\t' + wiki.get(parameter['WikiName'])

        elif program == 8:
            if function == 1:
                if type == 1:
                    ch = False
                    tell = self.analMsg(parameter['Tell'])
                    parameter['number'] = int(float(parameter['number']))
                    parameter['number1'] = int(float(parameter['number1']))
                    for k in self.users:
                        print(str(self.users[k]['dong']) + ' ' + str(parameter['number']) + ' ' + str(self.users[k]['ho']) + ' ' + str(parameter['number1']))
                        if self.users[k]['type'] == 0 and self.users[k]['dong'] == parameter['number'] and self.users[k]['ho'] == parameter['number1'] :
                            self.sendMessage(self.users[k]['client'], 'msg\ta\t{dong}동 {ho}호로 부터 메시지가 도착했습니다. {tell}'.format(dong=self.users[key]['dong'], ho=self.users[key]['ho'], tell=tell))
                            ch = True
                    if not ch:
                        return 'a\t해당 집 스피커가 접속 중이 아닙니다.'
                    return 'a\t{dong}동 {ho}호에게 {tell} 메시지를 보냈습니다.'.format(dong=parameter['number'], ho=parameter['number1'], tell=tell)
        return None


    def sendMessageForType(self, type, msg):
        for k in self.users:
            if self.users[k]['type'] == type:
                self.sendMessage(self.users[k]['client'], msg)

    def getUsersKey(self, client):
        for k in self.users:
            if self.users[k]['client'] == client:
                return k
        return None

    def getInClient(self, name, type, ho, dong):
        print(name, type, ho, dong)
        for key in self.users:
            print(str(key))
            if self.users[key]['name'] == name and self.users[key]['type'] == type and self.users[key]['ho'] == ho and self.users[key]['dong'] == dong:
                return key
        return None

    def getDoorlock(self, type, ho, dong):
        for key in self.users:
            print(str(key))
            if self.users[key]['type'] == type and self.users[key]['ho'] == ho and self.users[key]['dong'] == dong:
                return key
        return None

    def getUserClient(self, name):
        for k in self.users:
            if self.users[k]['name'] == name:
                return self.users[k]['client']
            else:
                return None

    def analMsg(self, string):
        a = ''
        if string.find('으라고', len(string) - 3) > 0:
            a = string.split('으라고')[0] + '어'
        elif string.find('오라고', len(string) - 3) > 0:
            a = string.split('오라고')[0] + '어'
        elif string.find('라고', len(string) - 2) > 0:
            a = string.split('라고')[0]
        elif string.find('고', len(string) - 1) > 0:
            a = string.split('고')[0]
        elif string.find('게', len(string) - 1) > 0:
            a = string.split('게')[0] + '자'
        elif string.find('로', len(string) - 1) > 0:
            a = string.split('로')[0]
        return a

