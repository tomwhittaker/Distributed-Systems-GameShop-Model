#thing that take data from client and sends to back end

from socket import *
from threading import *
from Custom import *

def placeOder():
    print ''
def retrieveOrderHistory():
    print ''
def cancelOrder():
    print ''
def connection(sock):
    print sock.recv(1024)
    while 1:
        if sock.getpeername()[0] != '127.0.0.1':
            break
        sentence = sock.recv(1024)
        numbers = sentence.split(' ')
        suma=0
        for x in numbers:
            suma = suma + int(x)
        sock.send(str(suma))

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(5)
print 'The server is ready to recieve'
while 1:
    connectionSocket, addr = serverSocket.accept()
    t = Thread(target = connection ,args=(connectionSocket,))
    t.setDaemon(1)
    t.start()
connectionSocket.close()
