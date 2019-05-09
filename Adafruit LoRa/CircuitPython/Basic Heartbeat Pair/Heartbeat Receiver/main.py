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

# Set up the onboard LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Set up the LoRa transmission
RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

heartbeats_missed = 0
MAX_MISSED_HEARTBEATS = 5

while (True):
    packet = rfm9x.receive(timeout=0.1)  # Wait for a packet to be received (up to 0.1 seconds)
    
    if packet is not None:
        packet_text = str(packet, 'ascii')
        print('Received: {0}'.format(packet_text))

        # Reset the heartbeat missed counter
        heartbeats_missed = 0
        led.value = False

    else:
        heartbeats_missed = heartbeats_missed + 1
        
        if heartbeats_missed < MAX_MISSED_HEARTBEATS:
            print('Have missed {:d} heartbeats'.format(heartbeats_missed))
            
        elif heartbeats_missed == MAX_MISSED_HEARTBEATS:
            print('Have missed {:d} heartbeats'.format(heartbeats_missed))
            print('Missed too many heartbeats.')
            led.value = True
            
