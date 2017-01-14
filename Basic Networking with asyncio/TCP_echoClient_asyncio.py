#! /usr/bin/env python

###############################################################################
# TCP_echoClient_asyncio.py
#
# Basic TCP server using the Python 3.5+ aysncio syntax
#
# Modified and extended from code at:
#  * https://docs.python.org/3/library/asyncio-protocol.html
#
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

import asyncio

# If installed, we can also use uvloop to dramatically speed up the server
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    # Just use the default asyncio loop
    print('Unable to import uvloop. Falling back to stock asyncio loop.') 

# Define the server IP address and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8888
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        """ Once connected, send the message """
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        """ Method is called when data is received """
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        """ Method is called when the connection is lost """
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()

# This check will allow us to run this multiple times in IPython, without 
# getting an error about the event loop being closed
if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()


message = 'Hello World!'

coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              SERVER_IP, SERVER_PORT)
loop.run_until_complete(coro)

loop.run_forever()
loop.close()