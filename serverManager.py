# -*- coding: utf-8 -*-

import socket
import threading
import naturalLanguage

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
        self.programs = programs
        self.db = programs['db']
        self.window = programs['window']

    def run(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.listenToClient, args=(client, address)).start()
            threading.Thread()

    def listenToClient(self, client, address):
        size = 1024

        key = int(client.recv(size).decode())
        if not self.addUser(key, client, address):
            client.close()
            return

        print('[System] %s [%d] %s 접속함' % (self.users[key]['address'], self.users[key]['id'], self.users[key]['name']))
        print('[System] 서버 클라이언트 수 [%d]' % len(self.users))
        '''
        while True:
            try:
                data = client.recv(size)
                if data:
                    self.searchProgram(client, str(data.decode()))
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
        while True:
            data = client.recv(size)
            if data:
                self.searchProgram(client, str(data.decode()))
            else:
                print('[System] %s %s 종료함' % (self.users[key]['address'], self.users[key]['address']))
                self.removeUser(key)
                client.close()
                print('[System] 서버 클라이언트 수 [%d]' % len(self.users))
                print('[System] Error: %s' % e)
                break


    def getSocket(self):
        return self.sock

    def serverClose(self):
        self.sock.close()

    def sendMessage(self, client, msg):
        print('전송: ' + msg)
        client.send(('server\t' + msg).encode())

    def addUser(self, key, client, address):
        if key in self.users:
            print('[Server] %d 이미 접속된 클라이언트\n' % key)
            return False
        result = self.db.executeQuery('select * from client where id = %s', (key,))
        if result is None:
            print('[Server] $s 등록되지 않은 클라이언트\n' % key)
            return False
        result = result[0]
        lock.acquire()
        self.users[key] = {'client':client, 'address':address, 'id':int(result[0]), 'name':result[1], 'type':int(result[2]), 'ho':int(result[3]), 'dong':int(result[4])}
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
                nal = naturalLanguage.NaturalLanguage(self.programs)
                key = self.getUsersKey(client)
                nal.analysisText(split_msg[2], self.users[key]['name'], self.users[key]['ho'], self.users[key]['dong'])
                self.sendMessage(client, 'msg\t' + nal.getMessage())
        elif split_msg[0] == "sensor":
            if split_msg[1] == "inputsql":
                # split_msg[2] 온도, split_msg[3] 습도, split_msg[4]가스
                self.db.updateQuery(
                    'insert into sensor values(%s, %s, %s, %s) on duplicate key '
                    'update temp = %s, humi = %s, gas = %s',
                    (self.getUsersName(client), split_msg[2], split_msg[3], split_msg[4], split_msg[2], split_msg[3],
                     split_msg[4]))
        elif split_msg[0] == "window":
            if split_msg[1] == "inputsql":
                #상태 온도 습도 강수량 미세먼지
                if split_msg[2] == "false":
                    split_msg[2] = False
                elif split_msg[2] == "true":
                    split_msg[2] = True
                self.db.updateQuery(
                    'insert into `window` values(%s, %s, %s, %s, %s, %s) on duplicate key '
                    'update `status` = %s and temp = %s and humi = %s and rain = %s and dust = %s',
                    (self.getUsersKey(client), split_msg[2], split_msg[3], split_msg[4], split_msg[5], split_msg[6],
                     split_msg[2], split_msg[3], split_msg[4], split_msg[5], split_msg[6]))
        elif split_msg[0] == "curtain":
            if split_msg[1] == "inputsql":
                # split_msg[2] 열림/닫힘, split_msg[3] 조도
                self.db.updateQuery(
                    'insert into sensor values((select id from client where name = %s), %s, %s) on duplicate key '
                    'update `status` = %s, lux = %s',
                    (self.getUsersName(client), split_msg[2], split_msg[3], split_msg[2], split_msg[3]))
        elif split_msg[0] == "doorlock":
            if split_msg[1] == "enroll":
                key = self.getUsersKey(client)
                self.db.updateQuery(
                    'insert into fingerprint values(%s, %s, %s, %s) on duplicate key '
                    'update finger = %s, dong_id = %s, ho_id = %s',
                    (key, split_msg[2], self.users[key]['dong'], self.users[key]['ho'], split_msg[2], self.users[key]['dong'], self.users[key]['ho']))

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
        for key in self.users:
            if self.users[key]['name'] == name and self.users[key]['type'] == type and self.users[key]['ho'] == ho and self.users[key]['dong'] == dong:
                return key
        return None

    def getUserClient(self, name):
        for k in self.users:
            if self.users[k]['name'] == name:
                return self.users[k]['client']
            else:
                return None


