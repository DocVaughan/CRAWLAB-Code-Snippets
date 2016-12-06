#! /usr/bin/env python

###############################################################################
# basic_serial_communication.py
#
# script to achieve basic send/receive communication
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/27/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import numpy as np
import logging
import serial
import time

logger = logging.getLogger(__name__)

# TODO: Make a nice class-based serial object for easier reuse
# class serial_comm(object):
#     ''' Class for sending/receiving serial data'''
#     def __init__(self, port):
#         self.port = port
#         self.ser = serial.Serial(port, 115200)
# 
#     # Sends throttle and steering angle commands to platform
#     def send_string(self, string):
#     
#         if type(string) is str:
#             # Write the data to the serial connection - to the Arudino for CAN bus formatting
#             self.ser.write(str(string))
#         else:
#             logging.debug('The send_string method requires a str type argument.')
#     
#     def __del__(self):
#         self.ser.close()
#     
    
if __name__ == '__main__':
    # serial port will have to change based on configuration
    PORT = '/dev/tty.usbserial-AK05G8CY'
    
    # define the serial communication parameters, 8 bits, no parity, 1 stop bit
    BPS = 115200
    
    # Define a Timeout for serial communication
    TIMEOUT = 0.01
    
    # Open the serial port
    ser = serial.Serial(PORT, BPS, timeout=TIMEOUT)
    
    time_start = time.time()

    try:
        while True:
            dt = time.time() - time_start
    
            data = 100 * np.sin(0.25*np.pi * dt)
        
            data_string = '{}\r\n'.format(int(data)).encode('utf-8')
        
            ser.write(data_string)
            print("Sending: {}".format(data_string))
            
            # We're assuming here that we get properly terminated lines 
            # over the serial connection. If we are not, either because they
            # are not properly terminated or we aren't receiving any data at
            # all, then this call will block indefinitely.
            line = ser.readline()
            print(line.decode('utf-8'))
            
            # Run the loop roughly every 0.1s, if all data is sent and received
            # without blocking
            time.sleep(0.1)


    except (KeyboardInterrupt, SystemExit):
        ser.close()
        