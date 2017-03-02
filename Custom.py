from __future__ import print_function
import Pyro4

global orderCounter
orderCounter=0

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
    def __init__(self, item, date):
      self.item = item
      self.canceled=False
      self.date = date
      global orderCounter
      self.id = orderCounter
      orderCounter=orderCounter+1

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
class Customer:
    """A simple customer class"""
    def __init__(self, name, address):
      self.name = name
      self.address = address
      self.orders = []
      self.canceledOrders = []

    def addOrder(self,order):
        self.orders.append(order)

    def getOrders(self):
        return self.orders

    def getCanceled(self):
        return self.canceledOrders

    def cancelOrder(self,order):
        self.orders.remove(order)
        order.cancelOrder()
        self.canceledOrders.append(order)

    def __str__(self):
        return self.name

    def check():
        print("Visited")
