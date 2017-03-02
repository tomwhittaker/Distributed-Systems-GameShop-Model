#thing that take data from client and sends to back end
from __future__ import print_function
from socket import *
from threading import *
from Custom import *
import cPickle as pickle
import Pyro4
import sys

items=[]
items.append(Item("For Honour",40))
items.append(Item("Dark Souls",20))
items.append(Item("Halo 3",15))
customer = Customer("Tom","123456")
order = Order(items[0],'1/1/1')
order2 = Order(items[1],'1/1/1')
order3 = Order(items[1],'1/1/1')
customer.addOrder(order)
customer.addOrder(order2)
customer.addOrder(order3)
customer.cancelOrder(order3)

def placeOder(sock):
    itemlist =pickle.dumps(items,-1)
    sock.send(itemlist) #3
    sentence = sock.recv(1024) #2
    num= int(sentence)
    item = items[num-1]
    name=item.getName()
    sock.send(name)#4
    sentence = sock.recv(1024) #3
    print(sentence)
    if sentence=='y':
        sock.send("Order Made")#5
    elif sentence == 'n':
        sock.send("Order Not Made")#5
    else:
        sock.send("invalid")#5print ''
def retrieveOrderHistory(sock):
    orderHistory =pickle.dumps(customer.getOrders(),-1)
    sock.send(orderHistory)
    cancled = pickle.dumps(customer.getCanceled(),-1)
    sock.send(cancled)
def cancelOrder(sock):
    orderHistory =pickle.dumps(customer.getOrders(),-1)
    sock.send(orderHistory)
    orderToCancel = sock.recv(1024)
    sentence = sock.recv(1024)
    if sentence == 'y':
        sock.send("Order Canceled")
    else:
        sock.send("Order not Canceled")

def connection(sock):
    while True:
        sentence = sock.recv(1024) #1
        print(sentence)
        if sentence=='a':
            placeOder(sock)
        if sentence=='b':
            retrieveOrderHistory(sock)
        if sentence=='c':
            cancelOrder(sock)
    sock.close()


# serverPort = 12001
# serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.bind(('localhost',serverPort))
# serverSocket.listen(5)
# print 'The server is ready to recieve'
# connectionSocket, addr = serverSocket.accept()
# connection(connectionSocket)
sys.excepthook = Pyro4.util.excepthook
ns = Pyro4.locateNS()
customer = Pyro4.Proxy("PYRONAME:example.customer")
customer.check()
