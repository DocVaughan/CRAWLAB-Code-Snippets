#! /usr/bin/env python

##########################################################################################
# UDP_broadcast.py
#
# simple UDP broadcast
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/15/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

# Send UDP broadcast packets
import socket
import threading
import time

MYPORT = 2390

import sys, time
# from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while 1:
    data = repr(time.time()) + '\n'
    s.sendto(data, ('<broadcast>', MYPORT))
    time.sleep(2)