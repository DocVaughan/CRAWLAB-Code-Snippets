#! /usr/bin/env python

###############################################################################
# main.py
#
# Script to test basic LoRa-MAC functionality on the LoPy boards from Pycom
#
# Modified code from:
#  https://docs.pycom.io/tutorials/lora/lora-mac
#
# Created: 09/11/18
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

from network import LoRa
import socket
import machine
import time

# Initialize the lora object and set the region to USA
lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)

# Set up a simple python socket to handle the LoRa packets
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

while True:
    # Set the socket to blocking and send a simple string
    lora_sock.setblocking(True)
    print('Sending Hello')
    lora_sock.send('Hello')

    # Set the socke to non-blocking and wait for 64 bytes of data
    lora_sock.setblocking(False)
    print('Waiting for data...')
    data = lora_sock.recv(64)

    # Then, print that data to the REPL
    print('Received: {}'.format(data))

    # Sleep for a random amount of time. This will allow two LoPys to run this
    # exact version of the code, reducing the possibility of multiple colliding
    # packets
    time.sleep(machine.rng() & 0x0F)
