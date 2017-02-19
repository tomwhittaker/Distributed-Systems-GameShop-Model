#Thing that gets typed in

from socket import *
from Custom import *
import cPickle as pickle



def placeOder(item):
    print ''

def retrieveOrderHistory():
    print ''

def cancelOrder():
    print ''

def menu(sock):
    print 'Ready'
    sentence = raw_input('Do you wish to access the online Game Shop? (y=yes and n=no)')
    if sentence=='n':
        sock.close()
    else:
        print sock.recv(1024) #a/b/c
        sentence = raw_input('')
        sock.send(sentence)
        sentence = sock.recv(1024)
        print sentence
        sentence = sock.recv(1024)
        items = pickle.loads(sentence)
        counter=1
        for x in items:

            print str(counter)+": ",x
            counter= counter+1
        sock.close()



serverName = 'localhost'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
menu(clientSocket)
