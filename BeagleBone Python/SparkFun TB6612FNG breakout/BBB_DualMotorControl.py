#! /usr/bin/env python

###############################################################################
# BBB_DualMotorControl.py
#
# Basic test of dual motor control using the SparkFun TB6612FNG breakout board
#  http://sfe.io/p9457
# 
# Requires - Adafruit BeagleBone IO Python library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/03/15
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
A01 = 'P8_7'        # A01 pin on board, controls direction along with A02
A02 = 'P8_8'        # A02 pin on board, controls direction along with A01
PWMA = 'P8_13'      # PWMA pin on board, controls the speed of Motor A
B01 = 'P8_9'        # B01 pin on board, controls direction along with B02
B02 = 'P8_10'       # B01 pin on board, controls direction along with B01
PWMB = 'P8_19'      # PWMB pin on board, controls the speed of Motor B
STBY = 'P8_11'      # STBY pin on the breakout, must go low to enable motion
E_STOP = 'P8_12'    # Pin of the swtich to turn the motor on


# Set up reading the E-stop switch
GPIO.setup(E_STOP, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


# Set up the GPIO pins as output
GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(A01, GPIO.OUT)
GPIO.setup(A02, GPIO.OUT)
GPIO.setup(B01, GPIO.OUT)
GPIO.setup(B02, GPIO.OUT)

# Standby pin should go high to enable motion
GPIO.output(STBY, GPIO.HIGH)

# A01 and A02 have to be opposite to move, toggle to change direction
# Up
# GPIO.output(A01, GPIO.HIGH)
# GPIO.output(A02, GPIO.LOW)
# GPIO.output(B01, GPIO.LOW)
# GPIO.output(B02, GPIO.HIGH)

# Down
GPIO.output(A01, GPIO.LOW)
GPIO.output(A02, GPIO.HIGH)
GPIO.output(B01, GPIO.HIGH)
GPIO.output(B02, GPIO.LOW)


# Start the motors
# PWM.start(channel, duty, freq=2000, polarity=0)
PWM.start(PWMA, 100)
PWM.start(PWMB, 100)

# optionally, change the PWM frequency and polarity from their defaults
# PWM.start("P9_14", 50, 1000, 1)

# Run the motor for 10s
time.sleep(0.5)

# Stop the motor and cleanup the PWM
PWM.stop(PWMA)
PWM.stop(PWMB)
PWM.cleanup()

# Make standby pin low to go back into standby mode
GPIO.output(STBY, GPIO.LOW)