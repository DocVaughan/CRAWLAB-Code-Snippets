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
#   * 05/10/16 - JEV - 05/10/16
#       - updated for Python 3
#
##########################################################################################

# Send UDP broadcast packets
import socket
import time

PORT = 2390
count = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s.bind(('', PORT))
# s.setblocking(0)

try:
    while 1:
        data = '{} \n'.format(count)
#         s.sendto(data.encode('utf-8'), ('<broadcast>', PORT))
        s.sendto(data.encode('utf-8'), ('255.255.255.255', PORT))
        print('Sending: {}'.format(data))

        # Increment counter for sending
        count = count + 1
    
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    s.close()