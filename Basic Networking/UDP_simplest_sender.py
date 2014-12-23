#! /usr/bin/env python

##########################################################################################
# UDP_simplest_sender.py
#
# simplest UDP sender possible
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 11/14/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import socket

UDP_IP = "192.168.10.1"
UDP_PORT = 10005
MESSAGE = "q"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
                     
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

