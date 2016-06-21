#! /usr/bin/env python

###############################################################################
# TCP_server_ThreadedStream.py
#
# script to test TCP connections to/from the multiple clients
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/18/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import socket
import socketserver
import threading
import time


CLIENT_1_ADDRESS = '192.168.0.20'
CLIENT_1_PORT = 2390

CLIENT_2_ADDRESS = '192.168.0.30'
CLIENT_2_PORT = 2390

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print("Received: {}".format(response))
    finally:
        sock.close()

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)


try:
    start_time = time.time()
    while True:
        dt = time.time() - start_time
        signal = 25 * np.sin(0.5 * np.pi * dt) + 25

        data = '{}\r\n'.format(int(signal))
        
        client(CLIENT_1_ADDRESS, CLIENT_1_PORT, data.encode('utf-8'))
        print('Sending to {}:{} \t Message: {}'.format(CLIENT_1_ADDRESS, CLIENT_1_PORT, data))
        time.sleep(0.04)
        
        # client(CLIENT_2_ADDRESS, CLIENT_2_PORT, data.encode('utf-8'))
        # print('Sending: {} to {}:{}'.format(data, CLIENT_2_ADDRESS, CLIENT_2_PORT))
        # time.sleep(0.04)
        
except (KeyboardInterrupt, SystemExit):
    server.shutdown()
