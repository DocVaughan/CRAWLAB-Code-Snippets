#! /usr/bin/env python

###############################################################################
# esp32_NeoPixel_KnightRider.py
#
# Simple Knight Rider effect using a neopixel strip connected to an esp32
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 02/02/19
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

import machine 
import neopixel
import time

NEO_PIN = 15
NUM_LEDS = 60
NUM_CYCLE = 5

RED_HIGH = (255,0,0)
RED_LOW = (16,0,0)
GREEN_HIGH = (0,255,0)
GREEN_LOW = (0,16,0)
BLUE_HIGH = (0,0,255)
BLUE_LOW = (0,0,16)


neo = neopixel.NeoPixel(machine.Pin(NEO_PIN), NUM_LEDS)

# Should be filled with 0s to start (off), but ensure that's true
neo.fill((0,0,0))
neo.write()


index = 0
going = True

while(True):
    # Fill with zeros (off) to start
    neo.fill(RED_LOW)

    if (index + NUM_CYCLE >= NUM_LEDS):
        going = False
         
    elif (index <= 0):
        going = True


    
    if going:
        for n in range(NUM_CYCLE):
            neo[index + n] = RED_HIGH
        
        index = index + 1

    else:
        for n in range(NUM_CYCLE):
            neo[index + NUM_CYCLE - n - 1] = RED_HIGH

        index = index - 1

    neo.write()
#     for led_number, led in enumerate(led_state):
#         led_def = 'LED{}'.format(led_number)
#         if led:
#             v[led_def].background_color='red'
#         else:
#             v[led_def].background_color='cccccc'

    time.sleep(0.01)
