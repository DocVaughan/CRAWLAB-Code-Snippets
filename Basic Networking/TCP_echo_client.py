#! /usr/bin/env python

###############################################################################
# TCP_echo_client.py
#
# Simple echo client using sockets
#
# Modified/extended from code at:
#  - https://pymotw.com/2/socket/tcp.html
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/13/17
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

import socket

# Define the server IP address and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8888
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

# Create a TCP/IP socket and connect it
# to the port where the server is listening
sock = socket.create_connection(SERVER_ADDRESS)
print('connecting to {} on port {}'.format(SERVER_IP, SERVER_PORT))

try:
    # Send data
    message = 'This is the message.'
    print('sending {}'.format(message))
    
    # In Python 3, we need to specify the encoding of the string
    sock.sendall(message.encode('utf-8'))

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('Received {}'.format(data))

finally:
    print('Now, closing socket.')
    sock.close()