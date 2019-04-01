# -*- coding: utf-8 -*-

import socket
import threading
import naturalLanguage

lock = threading.Lock()


class ServerManager(threading.Thread):
    def __init__(self, host, port, programs):
        threading.Thread.__init__(self)
        
        self.users = {}
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.programs = programs;
        self.db = programs['db'];
        
    def run(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            
    def listenToClient(self, client, address):
        size = 1024
        
        username = str(client.recv(size).decode())
        if self.addUser(username, client, address) == False :
            client.close()
            return ;
        
        print('[System] %s %s 접속함' %(username, self.users[username][1]))
        print('[System] 서버 클라이언트 수 [%d]' %len(self.users))
        
        
        while True:
            try:
                data = client.recv(size)
                if data:
                    self.searchProgram(client, str(data.decode()))
                else:
                    raise ValueError('클라이언트 종료')
            except  Exception as e:
                print('[System] %s %s 종료함' %(username, self.users[username][1]))
                self.removeUser(username)
                client.close()
                print('[System] 서버 클라이언트 수 [%d]' %len(self.users))
                print('[System] Error: %s' %e)
                break
            
    def getSocket(self):
        return self.sock
    
    def serverClose(self):
        self.sock.close()
            
    def sendMessage(self, client, msg):
        client.send(('server|' + msg).encode())
        
    def addUser(self, username, client, address):
        if username in self.users:
            print('[Server] %s 이미 접속된 닉네임\n' %username)
            return False
        if self.db.executeQuery('select * from client where name = %s', (username,)) == None:
            print('[Server] $s 등록되지 않은 닉네임\n' %username)
            return False
            
        lock.acquire()
        self.users[username] = (client, address)
        lock.release()
        return True
    
    def removeUser(self, username):
        if username not in self.users:
            return
        lock.acquire()
        del self.users[username]
        lock.release() 
    
    def searchProgram(self, client, msg):
        split_msg = msg.split("\t")
        if split_msg[0] == "speaker":
            if split_msg[1] == "nal":
                nal = naturalLanguage.NaturalLanguage(self.programs)
                self.sendMessage(client, nal.analysisText(split_msg[2]))
        else if split_msg[0] == "insensor":
            if split_msg[1] == "inputsql":
                pass
        else  if split_msg[0] == "window":
            if split_msg[1] == "inputsql":
                pass
        else  if split_msg[0] == "curtain":
            if split_msg[1] == "inputsql":
                pass