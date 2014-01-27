import socket
import threading
import SocketServer
import time

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        string_to_print = "Velocity from {}: ".format(self.client_address[0]) + data
        print string_to_print
        socket.sendto(data.upper(), self.client_address)
        self.data = data

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
        

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "130.70.157.125", 2390
    
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address
    
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    
    # we can now count and receive UDP packets at the same time
    for ii in range(1,100):
        print ThreadedUDPRequestHandler.data
        print ii
        time.sleep(1)

    #   server.shutdown()