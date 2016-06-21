#! /usr/bin/env python

###############################################################################
# UDP_server_Threaded.py
#
# Threaded UDP server
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/27/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

# Allow use (maybe) in Python 2
from __future__ import print_function

import socket
import threading
import socketserver
import time

# TODO: Fix this nasty global variable hack
data, x_data, y_data = None, None, None

# Send some data to start communication?
SEND_DATA = False

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
        global data #x_data, y_data
        data = self.request[0].strip()
        socket = self.request[1]
        string_to_print = "Data from {}: {}".format(self.client_address, data)
        print(string_to_print)
#         x,sep,y = data.partition(',')
#         x_data = float(x)
#         y_data = float(y)
        
#         socket.sendto(string_to_print.encode('utf-8'), self.client_address)

# Streaming?... change above to SocketServer.StreamRequestHandler
#     def handle(self):
#         # self.rfile is a file-like object created by the handler;
#         # we can now use e.g. readline() instead of raw recv() calls
#         self.data = self.rfile.readline().strip()
#         print "{} wrote:".format(self.client_address[0])
#         print self.data
#         # Likewise, self.wfile is a file-like object used to write back
#         # to the client
#         self.wfile.write(self.data.upper())
        

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == '__main__':
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = '10.0.1.6', 2390
    
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address
    
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target = server.serve_forever)
    
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    
    server_thread.start()
    print('Server loop running in thread: {}'.format(server_thread.name))
        
        
    # we can now count and receive UDP packets at the same time
    try:
        if SEND_DATA:
            UDP_TARGET_IP = '10.0.1.99'
            UDP_PORT = 2390
            MESSAGE = 'Hello from the Python server'
        
            send_sock = socket.socket(socket.AF_INET,    # Internet
                                      socket.SOCK_DGRAM) # UDP
                     
            send_sock.sendto(MESSAGE.encode('utf-8'), (UDP_TARGET_IP, UDP_PORT))
    
        while True:
            if SEND_DATA:
                send_sock.sendto(MESSAGE.encode('utf-8'), (UDP_TARGET_IP, UDP_PORT))
            
            time.sleep(0.1)
            
    except (KeyboardInterrupt, SystemExit): 
        print('Waiting for server to shtudown and close...')
        server.socket.close()
        server.shutdown()
        server_thread.join(2) # Wait for the server thread to terminate
        server.server_close()
        print('Closing...')