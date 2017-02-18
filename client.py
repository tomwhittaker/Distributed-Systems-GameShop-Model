#Thing that gets typed in

from socket import *
from Custom import *



def placeOder(item):
    print ''

def retrieveOrderHistory():
    print ''

def cancelOrder():
    print ''





serverName = 'localhost'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print 'Ready'
while 1:
    sentence = raw_input('Input 5 numbers seperated by spaces ')
    if sentence=="x":
        break
    clientSocket.send(sentence)
    modifiedSentence = clientSocket.recv(1024)
    print "From Server:", modifiedSentence
clientSocket.close()
