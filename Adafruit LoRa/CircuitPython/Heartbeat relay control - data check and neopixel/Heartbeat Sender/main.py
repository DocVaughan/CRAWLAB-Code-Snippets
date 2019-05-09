#! /usr/bin/env python

###############################################################################
# main.py
#
# Basic sending of heartbeat signal using Adafruit LoRA feathers
#
#
# Created: 05/04/19
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

import digitalio
import board
import busio
import time
import adafruit_rfm9x

# Set up the LoRa transmission
RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

while (True):
    rfm9x.send('$ULheartbeat')
    
#     print('Waiting for data...')
#     packet = rfm9x.receive(timeout_s=0.1)  # Wait for a packet to be received (up to 0.5 seconds)
#     if packet is not None:
#         packet_text = str(packet, 'ascii')
#         print('Received: {0}'.format(packet_text))
    
    time.sleep(0.05)
