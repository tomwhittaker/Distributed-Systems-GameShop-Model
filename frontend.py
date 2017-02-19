#thing that take data from client and sends to back end

from socket import *
from threading import *
from Custom import *
import cPickle as pickle

items=[]
items.append(Item("For Honour",40))
items.append(Item("Dark Souls",20))
items.append(Item("Halo 3",15))


def placeOder():
    print ''
def retrieveOrderHistory():
    print ''
def cancelOrder():
    print ''
def connection(sock):
    sock.send("Would you like to a)make an order, b)retrieve your order history or c) cancel an order?")
    sentence = sock.recv(1024)
    if sentence=='a':
        sock.send("Which item would you like?")
        itemlist =pickle.dumps(items,-1)
        sock.send(itemlist)
    if sentence=='b':
        sock.send(sentence)
    if sentence=='c':
        sock.send(sentence)


serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(5)
print 'The server is ready to recieve'
connectionSocket, addr = serverSocket.accept()
connection(connectionSocket)
connectionSocket.close()
