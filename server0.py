#deals with shit
from __future__ import print_function
from Custom import *
import Pyro4
import Pyro4.naming
import Pyro4.core
import socket
import time
import select
import sys

def main():
    # sys.excepthook = Pyro4.util.excepthook
    Pyro4.config.SERIALIZERS_ACCEPTED = {'json','marshal','serpent','pickle'}
    server0=Server('efgsd','gdsda')
    Pyro4.Daemon.serveSimple(
    {
        server0: "server0",
        # Item: "item",
        # Order:"order"
    },
    ns=True)


if __name__=="__main__":
    main()
