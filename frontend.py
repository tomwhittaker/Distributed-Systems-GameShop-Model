#thing that take data from client and sends to back end
from socket import *
from threading import *
from Custom import *
import cPickle as pickle
import Pyro4
import sys
import time

itemsL=[]
itemsL.append(Item("For Honour",40))
itemsL.append(Item("Dark Souls",20))
itemsL.append(Item("Halo 3",15))

# customer = Customer("Tom","123456")
# order = Order(items[0],'1/1/1')
# order2 = Order(items[1],'1/1/1')
# order3 = Order(items[1],'1/1/1')
# customer.addOrder(order)
# customer.addOrder(order2)
# customer.addOrder(order3)
# customer.cancelOrder(order3)

def placeOder(sock,user):
    global items
    global server
    items=[]
    counter=0
    another=True
    itemlist =pickle.dumps(itemsL,-1)
    sock.send(itemlist) #1s
    while another:
        sentence = sock.recv(1024) #2r
        num= int(sentence)
        item = itemsL[num-1]
        name=item.getName()
        print(name)
        sock.send(name)#2s
        sentence = sock.recv(1024) #3r
        print(sentence)
        if sentence=='y':
            counter=counter+1
            items.append(item)
        if counter==3:
            another=False
            sock.send('False')#3s
        else:
            sock.send('True')#3s
        if another:
            sentence =sock.recv(1024)#4r
            if sentence=='n':
                another=False
    sentence = sock.recv(1024)#5r
    if sentence=='y':
        sock.send("Order Made")#4s
        print items
        print user
        try:
             server = connectionRMI()
        except Pyro4.errors.CommunicationError:
            port=(port+1)%3
            connectionRMI()
        server.addOrder(items,user)
    elif sentence == 'n':
        sock.send("Order Not Made")#4s
    else:
        sock.send("invalid")#4s
def retrieveOrderHistory(sock,user):
    global port
    global server
    try:
         server = connectionRMI()
    except Pyro4.errors.CommunicationError:
        port=(port+1)%3
        connectionRMI()
    print(server)
    orderHistory =pickle.dumps(server.getOrders(user),-1)
    sock.send(orderHistory) #1s
    try:
         server = connectionRMI()
    except Pyro4.errors.CommunicationError:
        port=(port+1)%3
        connectionRMI()
    cancled = pickle.dumps(server.getCanceled(user),-1)
    sock.send(cancled)#2s
def cancelOrder(sock,user):
    global port
    global server
    orderHistory =pickle.dumps(server.getOrders(user),-1)
    sock.send(orderHistory)#1s
    orderToCancel = sock.recv(1024)#2r
    sentence = sock.recv(1024)#3r
    if sentence == 'y':
        sock.send("Order Canceled")#2s
        try:
             server = connectionRMI()
        except Pyro4.errors.CommunicationError:
            port=(port+1)%3
            connectionRMI()
        server.cancelOrder(orderToCancel,user)
    else:
        sock.send("Order not Canceled")#2s

def connection(sock):
    global port
    global server
    sock.send("Please enter a username (If you have been using the store, one of our servers has disconnected and we apologise for the inconvience)") #0.5s
    sentence=sock.recv(1024) #0.5r
    print sentence
    try:
         server = connectionRMI()
    except Pyro4.errors.CommunicationError:
        port=(port+1)%3
        connectionRMI()
    server.setCurrentUser(sentence)
    user=sentence
    while True:
        sentence = sock.recv(1024) #1r
        print(sentence)
        if sentence=='a':
            placeOder(sock,user)
        if sentence=='b':
            retrieveOrderHistory(sock,user)
        if sentence=='c':
            cancelOrder(sock,user)
        if sentence=='x':
            break


    print("")
    print('testing')
    try:
        uri = 'PYRO:server0@localhost:50610'
        server = Pyro4.Proxy(uri)
        print('')
        print('1')
        print('')
        orders = server.getOrders(user)
        for x in orders:
            print "Order ",x.getId(),":"
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
        print ""
        orders = server.getCanceled(user)
        print "Cancled Orders:"
        for x in orders:
            print "Order ID: ",x.getId()
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
    except Pyro4.errors.CommunicationError:
        print('something has gone wrong')
    try:
        uri = 'PYRO:server1@localhost:50611'
        server = Pyro4.Proxy(uri)
        print('')
        print('2')
        print('')
        orders = server.getOrders(user)
        for x in orders:
            print "Order ",x.getId(),":"
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
        print ""
        orders = server.getCanceled(user)
        print "Cancled Orders:"
        for x in orders:
            print "Order ID: ",x.getId()
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
    except Pyro4.errors.CommunicationError:
        print('something has gone wrong')

    try:
        uri = 'PYRO:server2@localhost:50612'
        server = Pyro4.Proxy(uri)
        print('')
        print('3')
        print('')
        orders = server.getOrders(user)
        for x in orders:
            print "Order ",x.getId(),":"
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
        print ""
        orders = server.getCanceled(user)
        print "Cancled Orders:"
        for x in orders:
            print "Order ID: ",x.getId()
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
    except Pyro4.errors.CommunicationError:
        print('something has gone wrong')
    sock.close()


def getURIfromPort():
    global port
    ports=[50610,50611,50612]
    uri = 'PYRO:server'+str(ports[port])[-1:]+'@localhost:'+str(ports[port])
    return uri

def connectionRMI():
    global port
    global server
    uri = getURIfromPort()
    server = Pyro4.Proxy(uri)
    server.setMaster()
    server.check()
    return server

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(5)
print('The server is ready to recieve')
connectionSocket, addr = serverSocket.accept()
sys.excepthook = Pyro4.util.excepthook
Pyro4.config.SERIALIZERS_ACCEPTED = {'json','marshal','serpent','pickle'}
Pyro4.config.SERIALIZER = 'pickle'
#added to make master port variable
global port
port=0
try:
    connectionRMI()
except Pyro4.errors.CommunicationError:
    port=(port+1)%3
    connectionRMI()
connection(connectionSocket)
