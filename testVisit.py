from testWarehouse import Warehouse
from testPerson import Person
import Pyro4

warehouse = Pyro4.Proxy("PYRONAME:example.warehouse")
janet = Person("Janet")
henry = Person("Henry")
janet.visit(warehouse)
henry.visit(warehouse)
