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

# Set up the digital output to control the relay
relay = digitalio.DigitalInOut(board.D5)
relay.direction = digitalio.Direction.OUTPUT
relay.value = False

# Set up the LoRa transmission
RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

heartbeats_missed = 0
MAX_MISSED_HEARTBEATS = 5

while (True):
    # Wait for a packet to be received (up to timeout=0.1 seconds)
    packet = rfm9x.receive(timeout=0.1)  
    
    if packet is not None:
        try:
            packet_text = str(packet, 'ascii')
        
            # Now, check that the packet was actually the heartbeat packet
            if packet_text == '$ULheartbeat':
                print('Received: {0}'.format(packet_text))

                # Reset the heartbeat missed counter
                heartbeats_missed = 0
                led.value = not led.value    # toggle the onboard LED
                relay.value = True           # Keep the relay energized

            else: # If it wasn't still increment the missed counter
                heartbeats_missed = heartbeats_missed + 1

        except (UnicodeError):
            # If we can't properly parse the packet, consider it a missed
            # heartbeat
            heartbeats_missed = heartbeats_missed + 1 
    else:
        heartbeats_missed = heartbeats_missed + 1
        
    if heartbeats_missed > 0 and heartbeats_missed < MAX_MISSED_HEARTBEATS:
        print('Have missed {:d} heartbeats'.format(heartbeats_missed))
        
    elif heartbeats_missed == MAX_MISSED_HEARTBEATS:
        print('Have missed {:d} heartbeats'.format(heartbeats_missed))
        print('Missed too many heartbeats.')
        
        led.value = True     # Turn on the onboard red LED
        relay.value = False  # And de-energize the relay coils
