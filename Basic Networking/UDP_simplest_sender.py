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
#   * 01/27/16 - Joshua Vaughan - joshua.vaughan@louisiana.edu
#       - updated for Python 3
#
##########################################################################################

from __future__ import print_function

import socket

UDP_IP = '192.168.0.20'
UDP_PORT = 2390
MESSAGE = 'CRAWLAB'

print("UDP target IP: {}".format(UDP_IP))
print("UDP target port: {}".format(UDP_PORT))
print("Message: {}".format(MESSAGE))

sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP
                     
sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))

