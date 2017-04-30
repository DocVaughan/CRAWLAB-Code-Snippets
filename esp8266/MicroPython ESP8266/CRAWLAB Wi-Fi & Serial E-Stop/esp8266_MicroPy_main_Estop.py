#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_main_Estop.py
#
# main.py code for MicroPython running on the WemMos D1 Mini esp8266 board
# This script repeatedly checked a input which is connected to a hard-wired
# E-stop switch. If the E-stop is pressed, then the LED is lit and serial data
# is sent out
# 
# If the E-stop is not pressed, then the board does nothing
#
#
# The main.py file will run immediately after boot.py
# As you might expect, the main part of your code should be here
#
# Created: 04/30/17
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################


# This code should be in boot.py
# import machine
# # Create a pin object for the esp8266 onboard LED
# pin = machine.Pin(2, machine.Pin.OUT)

# Create a pin object for the esp8266 pin 0 - connected to WeMos D3
# Has 10k Pull-up resistor
pushbutton_pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)


# repeatedly check the E-stop, pushbutton_pin state
while True:
    # Button value will be low when closed
    if pushbutton_pin.value() == 0:
        pin.low()    # Turn on the LED
        print('STOP')
    else:
        pin.high()    # turn off the LED
    
    # sleep 0.1s between button reads
    time.sleep(0.1)