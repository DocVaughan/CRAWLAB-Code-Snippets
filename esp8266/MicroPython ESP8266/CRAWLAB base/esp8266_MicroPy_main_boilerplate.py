#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_main_boilerplate.py
#
# base main.py boilerplate code for MicroPython running on the esp8266
# Copy relevant parts and/or file with desired settings into main.py on the esp8266 
#
# The main.py file will run immediately after boot.py
# As you might expect, the main part of your code should be here
#
# Created: 06/04/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

# just blink the LED every 1s to indicate we made it into the main.py file
while True:
    time.sleep(1)
    pin.value(not pin.value()) # Toggle the LED while trying to connect
    time.sleep(1)