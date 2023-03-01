import re
import socket
import os

class TCP_Handler():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        if(not self.isConnectable()):
            print("Endereço invalido: substituindo por ip = 127.0.0.1 e porta = 53123")
            self.ip = '127.0.0.1'
            self.port = 53123

    def setIp(self,newIp):
        self.ip = newIp
    
    def setPort(self,newport):
        self.port = newport

    def StrIsIP(self):
        r = re.compile(('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'))
        if(r.match(self.ip) == None):
            print('ip invalido: formato invalido')
            return False
        return True
    
    def IsPortValid(self):
        try:
            int(self.port)
            if(len(self.port) > 6):
                print('porta invalida: mais de 6 digitos')
                return False 
            return True
        except:
            print('porta invalida: valor não numérico')
            return False

    def isConnectable(self):
        if(self.StrIsIP and self.IsPortValid):
            return True
        return False

    def connect(self):
        try:
            self.client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.client.settimeout(0.2)
            self.conn = self.client.connect( ( self.ip, self.port ) )
            self.client.settimeout(None)
            print(f'Conexão estabelicida: {self.ip}/{self.port}')

            return True
        except:
            print('Falha ao connectar')
            return False
            
    def disconnect(self):   
        try:
            print('disconnecting')
            self.client.close()
        except Exception as E:
            print(E)
            return
        
    def receive(self):
        return self.client.recv(8192).decode()

    def send(self,message):
        try:
            print(f'enviando: {message}')
            self.client.send(message.encode())
            return 1
        except:
            print('não enviado')
            return 0

    def sendACK(self):
        try:
            self.send("acknowledge")
            return 1
        except:
            return 0

    def systemFlow(self):
        while(1):
            data = self.receive()
            print(data)
            #escreve arquivos
            self.sendACK()

if( __name__ == '__main__'):
    htcp = TCP_Handler("127.0.0.1",53123)
    htcp.connect()
    htcp.sendACK()
    htcp.disconnect()

    