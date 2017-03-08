from __future__ import print_function
import Pyro4
import time

@Pyro4.expose
class Item:
    """A simple item class"""
    def __init__(self, name, cost):
      self.name = name
      self.cost = cost

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def getCost(self):
        return self.cost

    def __str__(self):
        return self.name

@Pyro4.expose
class Order:
    """A simple order class"""
    def __init__(self, items, date, orderId):
      self.canceled=False
      self.date = date
      global orderCounter
      self.id = orderId
      self.items = items

    def cancelOrder(self):
        self.canceled=True

    def getItem(self):
        return self.items

    def addItem(self,item):
        self.items.append(item)

    def getDate(self):
        return self.date

    def getCanceled(self):
        return self.canceled

    def getId(self):
        return self.id

    def getName(self):
        name =self.items[0].getName()
        return name

    def __str__(self):
        return self.items[0][0]

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server:
    """A simple server class"""
    def __init__(self,port,master):
      self.users={}
      self.orderCounter=0
      self.port = port
      self.master=master
      #added to so that the slaves are known to the master for whichever port is the master
      self.ports=[50610,50611,50612]
      self.ports.remove(port)

    def addOrder(self,items,user):
        print('addorder started')
        l=[]
        for x in items:
            l.append((x.getName(),x.getCost()))
        print('items created')
        order = Order(items,time.strftime("%d/%m/%Y"),self.orderCounter)
        self.users[user][0].append(order)
        self.orderCounter=self.orderCounter+1
        #propergate changes from master no matter which port is master
        if self.master:
            for x in self.ports:
                uri = 'PYRO:server'+str(x)[-1:]+'@localhost:'+str(x)
                print(uri)
                try:
                    server1 = Pyro4.Proxy(uri)
                    server1.createOrderAndItems(l,user)
                except Pyro4.errors.CommunicationError:
                    print('something has gone wrong')


    def createOrderAndItems(self,items,user):
        order = Order([],time.strftime("%d/%m/%Y"),self.orderCounter)
        for x in items:
            item = Item(x[0],x[0])
            order.addItem(item)
        self.users[user][0].append(order)
        self.orderCounter=self.orderCounter+1

    def getOrders(self,user):
        return self.users[user][0]

    def getCanceled(self,user):
        return self.users[user][1]

    def cancelOrder(self,orderId,user):
        for x in self.users[user][0]:
            if str(x.getId())==str(orderId):
                self.users[user][0].remove(x)
                x.cancelOrder()
                self.users[user][1].append(x)
                break
        #propergate changes from master no matter which port is master
        if self.master:
            for x in self.ports:
                uri = 'PYRO:server'+str(x)[-1:]+'@localhost:'+str(x)
                print(uri)
                try:
                    server1 = Pyro4.Proxy(uri)
                    server1.cancelOrder(orderId,user)
                except Pyro4.errors.CommunicationError:
                    print('something has gone wrong')



    def __str__(self):
        return self.name

    def check(self):
        print("Visited")
        return "Visited"

    def setCurrentUser(self,user):
        self.user=user
        if not self.users.has_key(user):
            self.users[user]=([],[])
            print("user created")
        #propergate changes from master no matter which port is master
        if self.master:
            for x in self.ports:
                uri = 'PYRO:server'+str(x)[-1:]+'@localhost:'+str(x)
                print(uri)
                try:
                    server1 = Pyro4.Proxy(uri)
                    server1.setCurrentUser(user)
                except Pyro4.errors.CommunicationError:
                    print('something has gone wrong')
        print(self.ports)

    def setMaster(self):
        print('set master begin')
        self.master=True
        print('set master')
        print(self.ports)
        #to allow you to change a port to master and others to slave
        for x in self.ports:
            print('set slave begin')
            uri = 'PYRO:server'+str(x)[-1:]+'@localhost:'+str(x)
            print(uri)
            try:
                server1 = Pyro4.Proxy(uri)
                print('connected')
                server1.setSlave()
            except Pyro4.errors.CommunicationError:
                print('something has gone wrong')
            print('slave set')


    def setSlave(self):
        self.master=False
