#Thing that gets typed in

from socket import *
from Custom import *
import cPickle as pickle



def placeOder(sock):
    run=True
    sentence = sock.recv(1024)#1r
    items = pickle.loads(sentence)
    counter=1
    for x in items:
        print str(counter)+": ",x
        counter= counter+1
    while run:
        print "Which item would you like? (Enter the item number)"
        sentence = str(raw_input(''))
        sock.send(sentence) #2s
        sentence = sock.recv(1024)#2r
        print "Please confirm you would like to order "+sentence+"? (y=yes and n=no)"
        sentence = str(raw_input(''))
        sock.send(sentence)#3s
        sentence = sock.recv(1024)#3r
        if sentence=="False":
            run=False
        if run:
            print "Would you like to buy another item? (y=yes and n=no)"
            sentence = str(raw_input(''))
            sock.send(sentence)#4s
            if sentence=='n':
                run=False
    print "Please can you confirm that you would like to make this order? (y=yes and n=no)"
    sentence = str(raw_input(''))
    sock.send(sentence)#5s
    sentence =sock.recv(1024)#4r
    print sentence

def retrieveOrderHistory(sock):
    sentence = sock.recv(1024)#1r
    history = pickle.loads(sentence)
    print "Orders:"
    for x in history:
        print "Order ",x.getId(),":"
        for y in x.getItem():
            print y.getName()
        print x.getDate()
        print ""
    can = sock.recv(1024)#2r
    canceled = pickle.loads(can)
    print ""
    print "Canceled Orders:"
    for x in canceled:
        print "Order ID: ",x.getId()
        for y in x.getItem():
            print y.getName()
        print x.getDate()
        print ""

def cancelOrder(sock):
    print "Do you know the order id? (y=yes and n=no)"
    sentence = str(raw_input(''))
    if sentence=='n':
        sentence = sock.recv(1024)#1r
        history = pickle.loads(sentence)
        for x in history:
            print "Order ",x.getId(),":"
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
    else:
        sentence = sock.recv(1024)#1r
        history = pickle.loads(sentence)
    print 'Which order would you like to cancel? (y=yes and n=no)'
    sentence = str(raw_input(''))
    sock.send(sentence)#2s
    name=''
    for x in history:
        if sentence == str(x.getId()):
            for y in x.getItem():
                name = name+ y.getName()+','
    name=name[:len(name)-1]
    print "Please confirm thay you would like to cancel your order of "+name+"? (y=yes and n=no)"
    sentence = str(raw_input(''))
    sock.send(sentence)#3s
    print sock.recv(1024)#2r

def menu(sock):
    print 'Ready'
    sentence = raw_input('Do you wish to access the online Game Shop? (y=yes and n=no)')
    if sentence=='n':
        sock.close()
    else:
        sentence = str(raw_input("Enter Username:"))
        sock.send(sentence)#0.5s
        while True:
            print "Would you like to a)make an order, b)retrieve your order history or c) cancel an order x)exit?"
            sentence = str(raw_input(''))
            sock.send(sentence)#1
            if (sentence=='a'):
                placeOder(sock)
            if (sentence=='b'):
                retrieveOrderHistory(sock)
            if (sentence=="c"):
                cancelOrder(sock)
            if (sentence=='x'):
                break
        sock.close()



serverName = 'localhost'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
menu(clientSocket)
