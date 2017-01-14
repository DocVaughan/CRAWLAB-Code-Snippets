#! /usr/bin/env python

###############################################################################
# UDP_client_asyncio.py
#
# Basic echo client, using the Python 3 asyncio module
# 
# The client sends a message to a server, then waits for a response. Once a 
# response is received, we close.
#
# Modified from code at:
#  https://docs.python.org/3/library/asyncio-protocol.html
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

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Sending:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print('Received:', data.decode())

        print('Now, close the socket.')
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('Socket closed, stopping the event loop.')
        loop = asyncio.get_event_loop()
        loop.stop()

loop = asyncio.get_event_loop()

# This check will allow us to run this multiple times in IPython, without 
# getting an error about the event loop being closed
if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()


message = 'Hello World!'

# For more info on the create_datagram_endpoint method, see:
#  https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.create_datagram_endpoint
connect = loop.create_datagram_endpoint(
                lambda: EchoClientProtocol(message, loop),
                remote_addr=('127.0.0.1', 2390))

transport, protocol = loop.run_until_complete(connect)

loop.run_forever()
transport.close()
loop.close()