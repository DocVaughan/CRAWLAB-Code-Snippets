#! /usr/bin/env python

##########################################################################################
# UDP_looping_sender.py
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

import numpy as np
import socket
import time

UDP_IP = '127.0.0.1'
UDP_PORT = 2390

print("UDP target IP: {}".format(UDP_IP))
print("UDP target port: {}".format(UDP_PORT))

sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP

try:
    start_time = time.time()
    while True:
        dt = time.time() - start_time
        signal = 25 * np.sin(0.5 * np.pi * dt) + 25

        data = '{}\r\n'.format(int(signal))
        sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))
        print('Sending: {}'.format(data))
    
        time.sleep(0.01)
except (KeyboardInterrupt, SystemExit):
    sock.close()
