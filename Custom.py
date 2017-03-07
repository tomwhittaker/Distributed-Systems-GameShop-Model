from __future__ import print_function
import Pyro4
import time

class Item:
    """A simple item class"""
    def __init__(self, name, cost):
      self.name = name
      self.cost = cost

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

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

    def __str__(self):
        return self.item

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server:
    """A simple server class"""
    def __init__(self, port):
      self.orders = []
      self.canceledOrders = []
      self.orderCounter=0
      self.port = port

    def addOrder(self,item):
        order = Order(item,time.strftime("%d/%m/%Y"),self.orderCounter)
        self.orders.append(order)
        self.orderCounter=self.orderCounter+1

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
