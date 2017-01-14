#! /usr/bin/env python

###############################################################################
# TCP_server_asyncio.py
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


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        """ Method is called once the connection with the client is made """
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        """ Method is called when data is received """
        message = data.decode()
        print('Data received: {!r}'.format(message))
        
        # Here, we just echo the message back to the sender
        print('Echoing: {!r}'.format(message))
        self.transport.write(data)

        # Then, we close the connection
        print('Close the client socket')
        self.transport.close()

# Create the asyncio event loop
loop = asyncio.get_event_loop()

if loop.isclosed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    

# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, SERVER_IP, SERVER_PORT)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()