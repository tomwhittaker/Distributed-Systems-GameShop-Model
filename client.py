#Thing that gets typed in

from socket import *
from Custom import *
import cPickle as pickle



def placeOder(sock):
    print "Which item would you like?"
    sentence = sock.recv(1024)
    items = pickle.loads(sentence)
    counter=1
    for x in items:
        print str(counter)+": ",x
        counter= counter+1
    sentence = raw_input('')
    sock.send(sentence) #2
    sentence = sock.recv(1024)
    print "Please confirm you would like to order "+sentence+"?"
    sentence = raw_input('')
    sock.send(sentence)
    sentence =sock.recv(1024)
    print sentence

def retrieveOrderHistory(sock):
    sentence = sock.recv(1024)
    history = pickle.loads(sentence)
    print "Orders:"
    for x in history:
        print "Order ",x.getId(),":"
        print x.getItem().getName()
        print x.getDate()
        print ""
    can = sock.recv(1024)
    canceled = pickle.loads(can)
    print ""
    print "Cancled Orders:"
    for x in canceled:
        print "Order ID: ",x.getId()
        print x.getItem().getName()
        print x.getDate()
        print ""

def cancelOrder(sock):
    print "Do you know the order id?"
    sentence = raw_input('')
    if sentence=='n':
        sentence = sock.recv(1024)
        history = pickle.loads(sentence)
        for x in history:
            print "Order ",x.getId(),":"
            print x.getItem().getName()
            print x.getDate()
            print ""
    else:
        sentence = sock.recv(1024)
        history = pickle.loads(sentence)
    print 'Which order would you like to cancel?'
    sentence = raw_input('')
    sock.send(sentence)
    name=''
    for x in history:
        if sentence == str(x.getId()):
            name=x.getItem().getName()
    print "Please confirm thay you would like to cancel your order of "+name+"?"
    sentence = raw_input('')
    sock.send(sentence)
    print sock.recv(1024)

def menu(sock):
    print 'Ready'
    sentence = raw_input('Do you wish to access the online Game Shop? (y=yes and n=no)')
    if sentence=='n':
        sock.close()
    else:
        while True:
            print "Would you like to a)make an order, b)retrieve your order history or c) cancel an order?"
            sentence = raw_input('')
            sock.send(sentence)
            if (sentence=='a'):
                placeOder(sock)
            if (sentence=='b'):
                retrieveOrderHistory(sock)
            if (sentence=="c"):
                cancelOrder(sock)
        sock.close()



serverName = 'localhost'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
menu(clientSocket)
