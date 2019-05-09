#! /usr/bin/env python

###############################################################################
# main.py
#
# basic test script of LoRA feathers
#
#
# Created: 05/03/19
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

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go (from 5) up to 23 dB:
rfm9x.tx_power = 13 

while (True):
    rfm9x.send('Hello from White!')
    
    print('Waiting for data...')
    packet = rfm9x.receive()  # Wait for a packet to be received (up to 0.5 seconds)
    if packet is not None:
        packet_text = str(packet, 'ascii')
        print('Received: {0}'.format(packet_text))
        
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
        rssi = rfm9x.rssi
        print('Received signal strength: {0} dB'.format(rssi))
    
    time.sleep(0.01)
