#! /usr/bin/env python 


# import socket
# from time import sleep
# 
# UDP_IP = "10.0.1.111"
# UDP_PORT = 2390
# MESSAGE = "Hello, World!"
# 
# print "UDP target IP:", UDP_IP
# print "UDP target port:", UDP_PORT
# print "message:", MESSAGE
# 
# while(1):
#     sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
#     sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
#     print "sending..."
#     sleep(2)
#     
# #     
import socket
import sys
from time import sleep

HOST, PORT = "10.0.1.112", 2390
# data = " ".join(sys.argv[1:])
data = "hello"

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while(1):
	# As you can see, there is no connect() call; UDP has no connections.
	# Instead, data is directly sent to the recipient via sendto().
	sock.sendto(data + "\n", (HOST, PORT))
	received = sock.recv(1024)

	print "Sent:     {}".format(data)
	print "Received: {}".format(received)
	sleep(2)
