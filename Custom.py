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

@Pyro4.expose
class Order:
    """A simple order class"""
    def __init__(self, item, date, orderId):
      self.item = item
      self.canceled=False
      self.date = date
      global orderCounter
      self.id = orderId

    def cancelOrder(self):
        self.canceled=True

    def getItem(self):
        return self.item

    def getDate(self):
        return self.date

    def getCanceled(self):
        return self.canceled

    def getId(self):
        return self.id

    def getName(self):
        item = self.getItem()
        name =item.getName()
        return name

    def __str__(self):
        return self.item

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server:
    """A simple server class"""
    def __init__(self, port,master):
      self.users={}
      self.orderCounter=0
      self.port = port
      self.master=master

    def addOrder(self,item):
        order = Order(item,time.strftime("%d/%m/%Y"),self.orderCounter)
        self.users[self.user][0].append(order)
        self.orderCounter=self.orderCounter+1
        if self.master:
            uri = 'PYRO:server1@localhost:50611'
            server1 = Pyro4.Proxy(uri)
            server1.createOrderAndItem(item.getName(),item.getCost())
            uri = 'PYRO:server2@localhost:50612'
            server2 = Pyro4.Proxy(uri)
            server2.createOrderAndItem(item.getName(),item.getCost())

    def createOrderAndItem(self,name,cost):
        item = Item(name,cost)
        order = Order(item,time.strftime("%d/%m/%Y"),self.orderCounter)
        self.users[self.user][0].append(order)
        self.orderCounter=self.orderCounter+1

    def getOrders(self):
        return self.users[self.user][0]

    def getCanceled(self):
        return self.users[self.user][1]

    def cancelOrder(self,orderId):
        for x in self.users[self.user][0]:
            if str(x.getId())==str(orderId):
                self.users[self.user][0].remove(x)
                x.cancelOrder()
                self.users[self.user][1].append(x)
                break
        if self.master:
            uri = 'PYRO:server1@localhost:50611'
            server1 = Pyro4.Proxy(uri)
            server1.cancelOrder(orderId)
            uri = 'PYRO:server2@localhost:50612'
            server2 = Pyro4.Proxy(uri)
            server2.cancelOrder(orderId)

    def getOrderItemName(self,orderId):
        for x in self.users[self.user][0]:
            if str(x.getId())==str(orderId):
                return x.getName()

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
        if self.master:
            uri = 'PYRO:server1@localhost:50611'
            server1 = Pyro4.Proxy(uri)
            server1.setCurrentUser(user)
            uri = 'PYRO:server2@localhost:50612'
            server2 = Pyro4.Proxy(uri)
            server2.setCurrentUser(user)
