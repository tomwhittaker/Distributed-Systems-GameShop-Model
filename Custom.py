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

    def cancelOrder(self):
        self.canceled=True

    def getItem(self):
        return self.item

    def getDate(self):
        return self.date

    def getCanceled(self):
        return self.canceled

    def __str__(self):
        return self.item

class Customer:
    """A simple customer class"""
    def __init__(self, name, address):
      self.name = name
      self.address = address
      self.orders = []

    def addOrder(self,order):
        self.orders.append(order)

    def getHistory(self):
        return self.orders

    def __str__(self):
        return self.name
