#! /usr/bin/env python

###############################################################################
# BBB_BasicMotorControl_Polulu.py
#
# Basic test of motor control using the Pololu High-power motor driver
#  https://www.pololu.com/product/755
#
# Requires - Adafruit BeagleBone IO Python library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/16/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time

# Set up the pins - These are mutable, but *don't* change them
DIR_PIN = 'P8_7'        # DIR pin on board, controls direction
PWM_PIN = 'P8_13'       # PWM pin on board, controls the speed of the motor 

# Set up the GPIO pins as output
GPIO.setup(DIR_PIN, GPIO.OUT)

# DIR high is one direction, DIR low is another
GPIO.output(DIR_PIN, GPIO.HIGH)

# Start the motor
# PWM.start(channel, duty, freq=2000, polarity=0)
PWM.start(PWM_PIN, 100)

# optionally, change the PWM frequency and polarity from their defaults
# PWM.start("P9_14", 50, 1000, 1)

# Run the motor for 10s
time.sleep(10)

# Stop the motor and cleanup the PWM
PWM.stop(PWM_PIN)
PWM.cleanup()