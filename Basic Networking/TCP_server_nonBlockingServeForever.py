import socket
import SocketServer
import threading
import time

data = []


class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global data
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
#         print "{} wrote:".format(self.client_address[0])
#         print self.data
        data = self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        # self.wfile.write(self.data.upper())

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True

if __name__ == '__main__':
    HOST, PORT = '10.0.1.121', 2390
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "\nServer loop running in thread:", server_thread.name

    # we can now count and receive TCP packets at the same time
    try:
        while True:
            print data
            time.sleep(0.1) 

    except (KeyboardInterrupt, SystemExit): 
        print 'Closing...'
        # Clean up
        server_thread.join(3)
        server.shutdown()
