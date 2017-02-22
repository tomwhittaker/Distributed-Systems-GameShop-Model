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
        print sock.recv(1024) #a/b/c #1
        sentence = raw_input('')
        if (sentence=='a'):
            sock.send(sentence) #1
            sentence = sock.recv(1024) #what item #2
            print sentence
            sentence = sock.recv(1024) #pickle #3
            items = pickle.loads(sentence)
            counter=1
            for x in items:
                print str(counter)+": ",x
                counter= counter+1
            sentence = raw_input('')
            sock.send(sentence) #2
            sentence = sock.recv(1024) #confirm #4
            print sentence
            sentence = raw_input('')
            sock.send(sentence) #3
            sentence =sock.recv(1024) #tell user their answer #5
            print sentence
        if (sentence=='b'):
            sock.send(sentence)
            sentence = sock.recv(1024)
            history = pickle.loads(sentence)
            counter=1
            print ""
            for x in history:
                print "Order ",counter,":"
                print x.getItem().getName()
                print x.getDate()
                if x.getCanceled():
                    print "Canceled"
                print ""
        if (sentence=="c"):
            print 'lol'
        sock.close()



serverName = 'localhost'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
menu(clientSocket)
