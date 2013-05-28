#! /usr/bin/env python 
 
import socket
import sys
from time import sleep

HOST, PORT = "10.0.1.111", 2390
# data = " ".join(sys.argv[1:])
data = 45

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while(1):
	# As you can see, there is no connect() call; UDP has no connections.
	# Instead, data is directly sent to the recipient via sendto().
	sock.sendto(str(data) + "\n", (HOST, PORT))
	received = sock.recv(1024)

	print "\nSent:     {}".format(data)
	print "Received: {}".format(received)
	
	data = data + 10
	if data > 150:
		data = 50
		
	sleep(1)
