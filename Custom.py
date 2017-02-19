class Item:
    """A simple item class"""
    def __init__(self, name, cost):
      self.name = name
      self.cost = cost

    def __str__(self):
        return self.name

class Order:
    """A simple order class"""
    def __init__(self, item):
      self.item = item
      canceled=False;

    def cancelOrder():
        canceled=True;

    def __str__(self):
        return self.item

class Customer:
    """A simple customer class"""
    def __init__(self, name, address):
      self.name = name
      self.address = address
      self.orders = []

    def addOrder(order):
        orders.append(order)

    def __str__(self):
        return self.name
