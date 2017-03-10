from __future__ import print_function
import Pyro4
import time
import ast

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

    def getCloneDetail(self):
        return self.name,self.cost

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

    def getCloneDetail(self):
        il = []
        for x in self.items:
            name,cost=x.getCloneDetail()
            item = Item(name,cost)
            il.append(item)
        return il,self.date,self.id

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
        return str(self.id)

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server:
    """A simple server class"""
    def __init__(self,port,master):
        self.backUpItems=[]
        self.users={}
        self.orderCounter=0
        self.port = port
        self.master=master
        self.nOrders=0
        self.nCOrders=0
        #added to so that the slaves are known to the master for whichever port is the master
        self.ports=[50610,50611,50612]
        self.ports.remove(port)

    def addOrder(self,items,user):
        l=[]
        for x in items:
            l.append((x.getName(),x.getCost()))
        order = Order(items,time.strftime("%d/%m/%Y"),self.orderCounter)
        self.users[user.encode()][0].append(order)
        self.orderCounter=self.orderCounter+1
        self.nOrders=self.nOrders+1
        #propergate changes from master no matter which server is master
        self.fail=[]
        if self.master:
            for x in self.ports:
                uri = 'PYRO:server@localhost:'+str(x)
                try:
                    server1 = Pyro4.Proxy(uri)
                    server1.createOrderAndItems(l,user.encode())
                except Pyro4.errors.CommunicationError:
                    print('CommunicationError')
                    self.fail.append(x)
        return self.fail

    def createOrderAndItems(self,items,user):
        self.nOrders=self.nOrders+1
        order = Order([],time.strftime("%d/%m/%Y"),self.orderCounter)
        for x in items:
            item = Item(x[0],x[0])
            order.addItem(item)
        self.users[user.encode()][0].append(order)
        self.orderCounter=self.orderCounter+1

    def getOrders(self,user):
        return self.users[user.encode()][0]

    def getCanceled(self,user):
        return self.users[user.encode()][1]

    def cancelOrder(self,orderId,user):
        for x in self.users[user.encode()][0]:
            if str(x.getId())==str(orderId):
                self.users[user.encode()][0].remove(x)
                x.cancelOrder()
                self.users[user.encode()][1].append(x)
                break
        self.nOrders=self.nOrders-1
        self.nCOrders=self.nCOrders+1
        #propergate changes from master no matter which server is master
        self.fail=[]
        if self.master:
            for x in self.ports:
                uri = 'PYRO:server@localhost:'+str(x)
                try:
                    server1 = Pyro4.Proxy(uri)
                    server1.cancelOrder(orderId,user.encode())
                except Pyro4.errors.CommunicationError:
                    print('CommunicationError')
                    self.fail.append(x)
        return self.fail

    def __str__(self):
        return self.name

    def check(self):
        return "Visited"

    def setCurrentUser(self,user):
        print(user)
        user=user.encode()
        self.user=user
        if not self.users.has_key(user):
            self.users[user]=([],[])
        #propergate changes from master no matter which servers is master
        if self.master:
            for x in self.ports:
                uri = 'PYRO:server@localhost:'+str(x)
                try:
                    server1 = Pyro4.Proxy(uri)
                    server1.setCurrentUser(user.encode())
                except Pyro4.errors.CommunicationError:
                    print('CommunicationError')

    def setMaster(self):
        self.master=True
        #to allow you to change a port to master and others to slave
        for x in self.ports:
            uri = 'PYRO:server@localhost:'+str(x)
            try:
                server1 = Pyro4.Proxy(uri)
                server1.setSlave()
            except Pyro4.errors.CommunicationError:
                print('CommunicationError')


    def setSlave(self):
        self.master=False

    def resetter(self,uri):
        server1 = Pyro4.Proxy(uri)
        server1.reset(self.orderCounter)
        for key, value in self.users.iteritems():
            server1.setCurrentUser(key)
            for x in value[0]:
                server1.clearBackUp()
                for y in x.getItem():
                    server1.resetaddItem(y.getName(),y.getCost())
                server1.resetAddOrder(x.getDate(),x.getId(),key)
                server1.clearBackUp()
            for x in value[1]:
                server1.clearBackUp()
                for y in x:
                    server1.resetaddItem(y.getName(),y.getCost())
                server1.resetAddCancelOrder(x.getDate(),x.getId(),key)
                server1.clearBackUp()

    def reset(self,orderCounter):
        print('reset')
        self.users={}
        self.master=False
        self.orderCounter=orderCounter

    def resetAddOrder(self,date,oId, user):
        order=Order(self.backUpItems, date, oId)
        self.users[user.encode()][0].append(order)

    def resetAddCancelOrder(self,date,oId, user):
        order=Order(self.backUpItems, date, oId)
        order.cancelOrder()
        self.users[user.encode()][1].append(order)

    def resetaddItem(self,name,cost):
        item=Item(name,cost)
        self.backUpItems.append(item)

    def clearBackUp(self):
        self.backUpItems=[]

    def setNumberOfOrders(self):
        self.nOrders=0
        self.nCOrders=0
        for key, value in self.users.iteritems():
            self.nOrders=self.nOrders+len(value[0])
            self.cNOrders=self.cNOrders+len(value[1])
        return self.nOrders, self.nCOrders

    def retNumberOfOrders(self):
        return self.nOrders, self.nCOrders

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Store:
    """A simple server class"""
    def __init__(self):
        self.itemsL=[]
        self.itemsL.append(Item("For Honour",40))
        self.itemsL.append(Item("Dark Souls",20))
        self.itemsL.append(Item("Halo 3",15))

    def getItemList(self):
        return self.itemsL
