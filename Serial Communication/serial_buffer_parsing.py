#! /usr/bin/env python

###############################################################################
# serial_buffer_parsing.py
#
# Basic parsing of a continous stream of serial data
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 12/04/16
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

# import from the future, so this should work identically in Python 2.7 and 3
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import matplotlib.pyplot as plt
import serial
import binascii

# serial port will have to change based on configuration
PORT = '/dev//tty.KeySerial1'

# define the serial communication parameters, 8 bits, no parity, 1 stop bit
BPS = 57600

ser = serial.Serial(PORT, BPS)
ser.flushInput()

# String that will hold the message to send over MQTT
serout_message = ''

try:
    while(True):
        ser_message = binascii.hexlify(ser.readline())

#         print('\n\n\n')
#         print(ser_message)
#         print('\n\n\n')
        
        if ser_message:
            # Now, check the message that was received. 
            if ser_message.endswith(b'\n'): # If we received a full line,
                # then print it
                print(ser_message)
        
                # and empty it
                # Note: This means we are losing data from some prior serial
                # commands that didn't complete with a newline. For some/many
                # applications this is probably okay. If not, you need to be
                # more careful here.
                serout_message = ''
        
                # Note: This also means that if a command is received in two “chunks”, 
                # with series of bytes is received without a newline, then the remainder 
                # with a newline, it will treat the second as the entire command. This 
                # could be remedied by simply checking for command format and/or length.

            elif ser_message != b'\n': 
                # else if the byte was not a newline character, append it to the 
                # mqtt_message. In this case, we are receiving a byte stream
                # and attempting to recreate the full string being sent. 
                # Micropython is basically Python3, so we need to indicate
                # the type of encoding for the message/string, decode it,
                # then append it to the existing message.
                serout_message = serout_message + ser_message.decode('utf-8')
                
            else:#  else the current byte we read was a newline
                # The newline indicates the end of a properly terminated message,
                # so we can send the message now.

                # Publish the message constructed from the byte sequence
                # MicroPython is basically Python3, so we need to indicate
                # the type of encoding for the message/string. 
                print(serout_message)
                
                # Then, empty the message
                serout_message = ''

except (KeyboardInterrupt, SystemExit):
    ser.close()