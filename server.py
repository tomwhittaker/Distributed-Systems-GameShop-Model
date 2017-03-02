#deals with shit
from __future__ import print_function
from Custom import *
import Pyro4.util
import Pyro4
import Pyro4.naming

def main():
    Pyro4.naming.startNSloop()
    Pyro4.Daemon.serveSimple(
            {
                Customer: "example.customer"
            },
            ns = True)
if __name__ == "__main__":
    main()
