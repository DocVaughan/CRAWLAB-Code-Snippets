#! /usr/bin/env python

###############################################################################
# UDP_server_asyncio.py
#
# Implementing a UDP server using the Python 3 asyncio asynchronous module instead of threads
#
# Code modified from that at:
#   https://docs.python.org/3/library/asyncio-protocol.html
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/11/17
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 01/13/17 - JEV - joshua.vaughan@louisiana.edu
#       - Added check for event loop to allow running repeatedly in IPython
#
# TODO:
#   * 
###############################################################################

import asyncio

HOST_IP, PORT = '127.0.0.1', 2390

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        """ This method gets called for each UDP packet received """
        message = data.decode()
        
        # Print out the message received 
        print('Received {} from {}'.format(message, addr))
        
        # and Echo it back to who sent it
        print('Sending {} to {}'.format(message, addr))
        self.transport.sendto(data, addr)

# Create the asyncio event loop
loop = asyncio.get_event_loop()

# This check will allow us to run this multiple times in IPython, without 
# getting an error about the event loop being closed
if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

print("Starting UDP server...")

# One protocol instance will be created to serve all client requests
# For more info on the create_datagram_endpoint method, see:
#  https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.create_datagram_endpoint
listen = loop.create_datagram_endpoint(EchoServerProtocol, 
                                       local_addr=(HOST_IP, PORT))

# Continue running the loop
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()