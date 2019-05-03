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

    def setPrograms(self, programs):
        self.programs = programs

    def run(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.listenToClient, args=(client, address)).start()
            threading.Thread()

    def listenToClient(self, client, address):
        size = 1024

        key = str(client.recv(size).decode())
        if not self.addUser(key, client, address):
            client.close()
            return

        print('[System] %s %s 접속함' % (self.users[key]['address'], self.users[key]['address']))
        print('[System] 서버 클라이언트 수 [%d]' % len(self.users))

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

    def getSocket(self):
        return self.sock

    def serverClose(self):
        self.sock.close()

    def sendMessage(self, client, msg):
        client.send(('server\t' + msg).encode())

    def addUser(self, key, client, address):
        if key in self.users:
            print('[Server] %d 이미 접속된 클라이언트\n' % key)
            return False
        result = self.programs['db'].executeQuery('select * from client where id = %s', (key,))
        if result is None:
            print('[Server] $s 등록되지 않은 클라이언트\n' % key)
            return False
        result = result[0]
        lock.acquire()
        self.users[key] = {'client':client, 'address':address, 'id':result[0], 'name':result[1], 'type':result[2], 'ho':result[3], 'dong':result[4]}
        lock.release()
        return True

    def removeUser(self, key):
        if key not in self.users:
            return
        lock.acquire()
        del self.users[key]
        lock.release()

    def searchProgram(self, client, msg):
        split_msg = msg.split("\t")
        if split_msg[0] == "speaker":
            if split_msg[1] == "nal":
                nal = naturalLanguage.NaturalLanguage(self.programs)
                nal.analysisText(split_msg[2], self.users[self.getUsersKey(client)]['name'], self.users[self.getUsersKey(client)]['ho'], self.users[self.getUsersKey(client)]['dong'])
                self.sendMessage(nal.getMessage())
        elif split_msg[0] == "sensor":
            if split_msg[1] == "inputsql":
                # split_msg[2] 온도, split_msg[3] 습도, split_msg[4]가스
                self.programs['db'].updateQuery(
                    'insert into sensor values((select id from client where name = %s), %s, %s, %s) on duplicate key '
                    'update temp = %s, humi = %s, gas = %s',
                    (self.getUsersName(client), split_msg[2], split_msg[3], split_msg[4], split_msg[2], split_msg[3],
                     split_msg[4]))
        elif split_msg[0] == "window":
            if split_msg[1] == "inputsql":
                self.window.setWindowsData(self.getUsersName(client), split_msg)
        elif split_msg[0] == "curtain":
            if split_msg[1] == "inputsql":
                # split_msg[2] 열림/닫힘, split_msg[3] 조도
                self.programs['db'].updateQuery(
                    'insert into sensor values((select id from client where name = %s), %s, %s) on duplicate key '
                    'update `status` = %s, lux = %s',
                    (self.getUsersName(client), split_msg[2], split_msg[3], split_msg[2], split_msg[3]))

    def getUsersKey(self, client):
        for k, v in self.users.items():
            if v['client'] == client:
                return k
            else:
                return None

    def sendMessageForType(self, type, msg):
        for k, v in self.users.items():
            if v['type'] == type:
                v['client'].send(('server\t' + msg).encode())

    def checkClientName(self, name, type, ho, dong):
        for user in self.users:
            if user['name'] == name and user['type'] == type and user['ho'] == ho and user['dong'] == dong:
                return True
        return False

    def getUsersName(self, client):
        for k, v in self.users.items():
            if v['client'] == client:
                return k
            else:
                return None

    def getUserClient(self, name):
        for k, v in self.users.items():
            if v['name'] == name:
                return v['client']
            else:
                return None


