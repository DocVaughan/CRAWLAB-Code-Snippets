import SocketServer

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        string_to_print = "Velocity from {}: ".format(self.client_address[0]) + data
        print string_to_print
        socket.sendto(data.upper(), self.client_address)

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

if __name__ == "__main__":
    HOST, PORT = '192.168.0.101', 2390
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()