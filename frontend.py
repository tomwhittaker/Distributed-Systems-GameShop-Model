#thing that take data from client and sends to back end
from socket import *
from threading import *
from Custom import *
import cPickle as pickle
import Pyro4
import sys
import time
import threading

# customer = Customer("Tom","123456")
# order = Order(items[0],'1/1/1')
# order2 = Order(items[1],'1/1/1')
# order3 = Order(items[1],'1/1/1')
# customer.addOrder(order)
# customer.addOrder(order2)
# customer.addOrder(order3)
# customer.cancelOrder(order3)
global items
global server
global ports
global crashed
global port


def placeOder(sock,user):
    global items
    global server
    global ports
    global crashed
    global port
    global itemsL
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
        sock.send(name)#2s
        sentence = sock.recv(1024) #3r
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
        try:
             server = connectionRMI()
        except Pyro4.errors.CommunicationError:
            crashed.append(ports[port])
            port=(port+1)%3
            connectionRMI()
        print(user)
        fail = server.addOrder(items,user.encode())
        if fail is not None:
            for x in fail:
                crashed.append(x)
    elif sentence == 'n':
        sock.send("Order Not Made")#4s
    else:
        sock.send("invalid")#4s
def retrieveOrderHistory(sock,user):
    global items
    global server
    global ports
    global crashed
    global port
    global itemsL
    try:
         server = connectionRMI()
    except Pyro4.errors.CommunicationError:
        crashed.append(ports[port])
        port=(port+1)%3
        connectionRMI()
    orderHistory =pickle.dumps(server.getOrders(user.encode()),-1)
    sock.send(orderHistory) #1s
    try:
         server = connectionRMI()
    except Pyro4.errors.CommunicationError:
        crashed.append(ports[port])
        port=(port+1)%3
        connectionRMI()
    cancled = pickle.dumps(server.getCanceled(user.encode()),-1)
    sock.send(cancled)#2s
def cancelOrder(sock,user):
    global items
    global server
    global ports
    global crashed
    global port
    global itemsL
    orderHistory =pickle.dumps(server.getOrders(user.encode()),-1)
    sock.send(orderHistory)#1s
    orderToCancel = sock.recv(1024)#2r
    sentence = sock.recv(1024)#3r
    if sentence == 'y':
        sock.send("Order Canceled")#2s
        try:
             server = connectionRMI()
        except Pyro4.errors.CommunicationError:
            crashed.append(ports[port])
            port=(port+1)%3
            connectionRMI()
        fail = server.cancelOrder(orderToCancel,user.encode())
        if fail is not None:
            for x in fail:
                crashed.append(x)
    else:
        sock.send("Order not Canceled")#2s

def connection(sock):
    global items
    global server
    global ports
    global crashed
    global port
    global itemsL
    sentence=sock.recv(1024) #0.5r
    try:
         server = connectionRMI()
    except Pyro4.errors.CommunicationError:
        crashed.append(ports[port])
        port=(port+1)%3
        connectionRMI()
    server.setCurrentUser(sentence.encode('ascii', 'ignore'))
    # crashed=[50610,50611,50612]
    user=sentence
    while True:
        sentence = sock.recv(1024) #1r
        if sentence=='a':
            placeOder(sock,user.encode())
        if sentence=='b':
            retrieveOrderHistory(sock,user.encode())
        if sentence=='c':
            cancelOrder(sock,user.encode())
        if sentence=='x':
            break


    print("")
    print('testing')
    try:
        uri = 'PYRO:server@localhost:50610'
        server = Pyro4.Proxy(uri)
        print('')
        print('1')
        print('')
        orders = server.getOrders(user.encode())
        for x in orders:
            print "Order ",x.getId(),":"
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
        print ""
        orders = server.getCanceled(user.encode())
        print "Cancled Orders:"
        for x in orders:
            print "Order ID: ",x.getId()
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
    except Pyro4.errors.CommunicationError:
        print('Server Down')
    try:
        uri = 'PYRO:server@localhost:50611'
        server = Pyro4.Proxy(uri)
        print('')
        print('2')
        print('')
        orders = server.getOrders(user.encode())
        for x in orders:
            print "Order ",x.getId(),":"
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
        print ""
        orders = server.getCanceled(user.encode())
        print "Cancled Orders:"
        for x in orders:
            print "Order ID: ",x.getId()
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
    except Pyro4.errors.CommunicationError:
        print('Server Down')

    try:
        uri = 'PYRO:server@localhost:50612'
        server = Pyro4.Proxy(uri)
        print('')
        print('3')
        print('')
        orders = server.getOrders(user.encode())
        for x in orders:
            print "Order ",x.getId(),":"
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
        print ""
        orders = server.getCanceled(user.encode())
        print "Cancled Orders:"
        for x in orders:
            print "Order ID: ",x.getId()
            for y in x.getItem():
                print y.getName()
            print x.getDate()
            print ""
    except Pyro4.errors.CommunicationError:
        print('Server Down')
    sock.close()


def getURIfromPort():
    global items
    global server
    global ports
    global crashed
    global port
    global itemsL
    uri = 'PYRO:server@localhost:'+str(ports[port])
    return uri

def connectionRMI():
    #added to reset fallen master server
    global items
    global server
    global ports
    global crashed
    global port
    global itemsL
    uri = getURIfromPort()
    server = Pyro4.Proxy(uri)
    server.setMaster()
    server.check()
    uriS = 'PYRO:Store@localhost:'+str(ports[port])
    store=Pyro4.Proxy(uriS)
    itemsL=store.getItemList()
    if not len(crashed)==0:
        for x in crashed:
            try:
                uri = 'PYRO:server@localhost:'+str(x)
                serverF = Pyro4.Proxy(uri)
                serverF.check()
                server.resetter(uri)
                crashed.remove(x)
                print('resetted server')
            except Pyro4.errors.CommunicationError:
                print 'still not working'
    return server



class myThread (threading.Thread):
    def __init__(self,connectionSocket):
        threading.Thread.__init__(self)
        self.connectionSocket = connectionSocket
    def run(self):
        global items
        global server
        global ports
        global crashed
        global port
        sys.excepthook = Pyro4.util.excepthook
        Pyro4.config.SERIALIZERS_ACCEPTED = {'json','marshal','serpent','pickle'}
        Pyro4.config.SERIALIZER = 'pickle'
        #added to make master port variable
        ports=[50610,50611,50612]
        crashed=[]
        port=0
        maxVal=[-1,-1]
        #added to make sure the port with the most up to date history is selected
        for x in range(0,3):
            try:
                uri = 'PYRO:server@localhost:'+str(ports[x])
                server = Pyro4.Proxy(uri)
                o,c = server.retNumberOfOrders()
                if c>maxVal[1]:
                    maxVal[1]=c
                    port=x
                if (o>maxVal[0]) or (o<maxVal[0] and c>maxVal[1]):
                    maxVal[0]=o
                    port=x
            except Pyro4.errors.CommunicationError:
                print('CommunicationError')
        #added to carry on attempting to conenct until it gets to a server which is not down
        try:
            connectionRMI()
        except Pyro4.errors.CommunicationError:
            crashed.append(ports[port])
            port=(port+1)%3
            connectionRMI()
        connection(self.connectionSocket)
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(5)
print('The server is ready to recieve')
threads=[]
while True:
    connectionSocket, addr = serverSocket.accept()
    thread = myThread(connectionSocket)
    thread.start()
    threads.append(thread)
