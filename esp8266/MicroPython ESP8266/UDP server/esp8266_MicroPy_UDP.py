#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_UDP.py
#
# Basic UDP networking for MicroPython running on the esp8266
# Paste this into the main.py on the board 
#
# The main.py file will run immediately after boot.py
# As you might expect, the main part of your code should be here
#
# Created: 06/04/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import socket
import network

# Configuration constants
UDP_TIMEOUT = 0.0               # Timeout for UDP communications (s), if 0 go into nonblocking mode
UDP_PORT = 2390                 # Port to receive data on
RECV_BUFF_SIZE = 16             # Size of buffer for UDP data
SEND_TO_IP = '192.168.4.2'      # Address to send to
SEND_TO_PORT = 2390             # Port to send data to


# Blink the LED every 100ms to indicate we made it into the main.py file
for _ in range(10):
    time.sleep_ms(100)
    pin.value(not pin.value()) # Toggle the LED while trying to connect
    time.sleep_ms(100)

# Make sure the LED is off
pin.high()

# Create the UDP socket
sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP

# Get the current IP address and port UDP_PORT information
# UDP_PORT is defined in config block at top of file
UDP_server_address = socket.getaddrinfo('0.0.0.0', UDP_PORT)[0][-1]
sock.bind(UDP_server_address)

# TODO: seems buggy right now, check again later
# create a timeout on UDP communication to avoid blocking forever
# sock.settimeout(UDP_TIMEOUT) 

# Create an address tuple to send data to 
# SEND_TO_IP and SEND_TO_PORT are defined in config block at top of file
send_to_address = socket.getaddrinfo(SEND_TO_IP, SEND_TO_PORT)[0][-1]

def UDP_recv():
    """ 
    Function to recveive data on UDP with a timeout and catch the timeout exception 
    
    Just prints the data received out to the REPL
    """
    try:
        data, addr = sock.recvfrom(RECV_BUFF_SIZE) # buffer size is 1024 bytes
        print(data)
    except (OSError):
        print('Receiving Timed Out')


def UDP_send(message):
    """ Function to send data on UDP with a timeout and catch the timeout exception 
    
    Arguments:
        message : the string to send
    
    Returns:
        none
    """
    try:
        _ = sock.sendto(message, send_to_address)
    except (OSError):
        print('Sending Timed Out')
        

# define a time, because we only want to send every 1s but received as fast as possible
last_time = time.time()


try:
    while True:
        # always be receiving
        UDP_recv()

        # Send Hello to SEND_TO_IP every 1s
        if time.time() - last_time > 1.0:
            # Send some data
            UDP_send('Hello')
            last_time = time.time()

except (KeyboardInterrupt, SystemExit):
    sock.close()