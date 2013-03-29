import xmlrpclib
import errno
import socket
import time
from OrdinaryNode.slivers import  extract_data as info

from OrdinaryNode.conn import conn_settings as set


max=0

def retry():

    global max
    time.sleep(set.sleep)
    if max != 0:
        max = max - 1
        main()
    else:
        raise

def main():
    proxy = xmlrpclib.ServerProxy(set.SN_IP+":"+set.SN_PORT)

    capacity = info.num_of_lxcs()

    try:
        res = proxy.register(10,4) #capacity, capacity)
        print res
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED  or e.errno == 101:
            print "SERVER is not Working"
            retry()
        else:
            print "Connection Problem"
            raise

def start():
    global max
    max = set.retry_max
    main()