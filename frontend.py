#thing that take data from client and sends to back end
from socket import *
from threading import *
from Custom import *
import cPickle as pickle
import Pyro4
import sys
import time

items=[]
items.append(Item("For Honour",40))
items.append(Item("Dark Souls",20))
items.append(Item("Halo 3",15))

# customer = Customer("Tom","123456")
# order = Order(items[0],'1/1/1')
# order2 = Order(items[1],'1/1/1')
# order3 = Order(items[1],'1/1/1')
# customer.addOrder(order)
# customer.addOrder(order2)
# customer.addOrder(order3)
# customer.cancelOrder(order3)

def placeOder(sock,server):
    itemlist =pickle.dumps(items,-1)
    sock.send(itemlist) #1s
    sentence = sock.recv(1024) #2r
    num= int(sentence)
    item = items[num-1]
    name=item.getName()
    print(name)
    sock.send(name)#2s
    sentence = sock.recv(1024) #3r
    print(sentence)
    if sentence=='y':
        sock.send("Order Made")#3s
        server.addOrder(item)
    elif sentence == 'n':
        sock.send("Order Not Made")#3s
    else:
        sock.send("invalid")#5print ''
def retrieveOrderHistory(sock,server):
    orderHistory =pickle.dumps(server.getOrders(),-1)
    sock.send(orderHistory) #1s
    cancled = pickle.dumps(server.getCanceled(),-1)
    sock.send(cancled)#2s
def cancelOrder(sock,server):
    orderHistory =pickle.dumps(server.getOrders(),-1)
    sock.send(orderHistory)#1s
    orderToCancel = sock.recv(1024)#2r
    sentence = sock.recv(1024)#3r
    if sentence == 'y':
        sock.send("Order Canceled")#2s
        server.cancelOrder(orderToCancel)
    else:
        sock.send("Order not Canceled")#2s

def connection(sock,server):
    sentence=sock.recv(1024) #0.5r
    server.setCurrentUser(sentence)
    while True:
        sentence = sock.recv(1024) #1r
        print(sentence)
        if sentence=='a':
            placeOder(sock,server)
        if sentence=='b':
            retrieveOrderHistory(sock,server)
        if sentence=='c':
            cancelOrder(sock,server)
        if sentence=='x':
            break
    print("")
    print('testing')
    uri = 'PYRO:server0@localhost:50610'
    server = Pyro4.Proxy(uri)
    print('')
    print('1')
    print('')
    orders = server.getOrders()
    for x in orders:
        print "Order ",x.getId(),":"
        print x.getItem().getName()
        print x.getDate()
        print ""
    print ""
    orders = server.getCanceled()
    print "Cancled Orders:"
    for x in orders:
        print "Order ID: ",x.getId()
        print x.getItem().getName()
        print x.getDate()
        print ""

    uri = 'PYRO:server1@localhost:50611'
    server = Pyro4.Proxy(uri)
    print('')
    print('2')
    print('')
    orders = server.getOrders()
    for x in orders:
        print "Order ",x.getId(),":"
        print x.getItem().getName()
        print x.getDate()
        print ""
    print ""
    orders = server.getCanceled()
    print "Cancled Orders:"
    for x in orders:
        print "Order ID: ",x.getId()
        print x.getItem().getName()
        print x.getDate()
        print ""
    uri = 'PYRO:server2@localhost:50612'
    server = Pyro4.Proxy(uri)
    print('')
    print('3')
    print('')
    orders = server.getOrders()
    for x in orders:
        print "Order ",x.getId(),":"
        print x.getItem().getName()
        print x.getDate()
        print ""
    print ""
    orders = server.getCanceled()
    print "Cancled Orders:"
    for x in orders:
        print "Order ID: ",x.getId()
        print x.getItem().getName()
        print x.getDate()
        print ""
    sock.close()


serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(5)
print('The server is ready to recieve')
connectionSocket, addr = serverSocket.accept()
# sys.excepthook = Pyro4.util.excepthook
Pyro4.config.SERIALIZERS_ACCEPTED = {'json','marshal','serpent','pickle'}
Pyro4.config.SERIALIZER = 'pickle'
uri = 'PYRO:server0@localhost:50610'
server = Pyro4.Proxy(uri)
print(1)
print(type(server))
connection(connectionSocket,server)
