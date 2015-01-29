#! /usr/bin/env python

###############################################################################
# BBB_blindLED.py
#
# script to blink an LED on the BeagleBone Black
#
# From: https://learn.adafruit.com/blinking-an-led-with-beaglebone-black/writing-a-program
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/09/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import Adafruit_BBIO.GPIO as GPIO
import time

# Define the pin used for the LED - This is mutable in python, so be careful
LED1 = 'P8_10'

# Set up the 'P8_10' pin as output
GPIO.setup(LED1, GPIO.OUT)

while True:
    GPIO.output(LED1, GPIO.HIGH)
    time.sleep(0.5)
    
    GPIO.output(LED1, GPIO.LOW)
    time.sleep(0.5)
