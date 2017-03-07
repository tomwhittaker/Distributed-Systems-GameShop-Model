#deals with shit
from __future__ import print_function
from Custom import *
import Pyro4
import Pyro4.naming
import Pyro4.core
import socket
import time
import select
import sys

def main():
    Pyro4.config.SERIALIZER = 'pickle'
    Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
    hostname=socket.gethostname()
    nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=hostname)
    pyrodaemon=Pyro4.core.Daemon(host=hostname)
    serveruri=pyrodaemon.register(Server('master','jtyfibk'))
    nameserverDaemon.nameserver.register("example.server",serveruri)
    while True:
        nameserverSockets = set(nameserverDaemon.sockets)
        pyroSockets = set(pyrodaemon.sockets)
        rs=[broadcastServer]
        rs.extend(nameserverSockets)
        rs.extend(pyroSockets)
        rs,_,_ = select.select(rs,[],[],3)
        eventsForNameserver=[]
        eventsForDaemon=[]
        for s in rs:
            if s is broadcastServer:
                print("Broadcast server received a request")
                broadcastServer.processRequest()
            elif s in nameserverSockets:
                eventsForNameserver.append(s)
            elif s in pyroSockets:
                eventsForDaemon.append(s)
        if eventsForNameserver:
            print("Nameserver received a request")
            nameserverDaemon.events(eventsForNameserver)
        if eventsForDaemon:
            print("Daemon received a request")
            pyrodaemon.events(eventsForDaemon)
    nameserverDaemon.close()
    broadcastServer.close()
    pyrodaemon.close()

if __name__=="__main__":
    main()
