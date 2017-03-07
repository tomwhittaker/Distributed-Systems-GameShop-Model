from __future__ import print_function
import Pyro4
import time

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Item:
    """A simple item class"""
    def __init__(self, name, cost):
      self.name = name
      self.cost = cost

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
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
      self.orders = []
      self.canceledOrders = []
      self.orderCounter=0
      self.port = port
      self.master=master

    def addOrder(self,item):
        order = Order(item,time.strftime("%d/%m/%Y"),self.orderCounter)
        self.orders.append(order)
        self.orderCounter=self.orderCounter+1
        if self.master:
            uri = 'PYRO:server1@localhost:50611'
            server = Pyro4.Proxy(uri)
            server.addOrder(item)
            uri = 'PYRO:server2@localhost:50612'
            server = Pyro4.Proxy(uri)
            server.addOrder(item)

    def getOrders(self):
        return self.orders

    def getCanceled(self):
        return self.canceledOrders

    def cancelOrder(self,orderId):
        for x in self.orders:
            if str(x.getId())==orderId:
                self.orders.remove(x)
                x.cancelOrder()
                self.canceledOrders.append(x)
                break

    def __str__(self):
        return self.name

    def check(self):
        print("Visited")
        return "Visited"
