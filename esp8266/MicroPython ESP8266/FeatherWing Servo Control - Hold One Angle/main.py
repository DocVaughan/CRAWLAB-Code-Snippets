###############################################################################
# main.py
#
# main script for servo control to hold one angle using an Adafruit esp8266 
# feather with their 8-channel PWM/servo FeatherWing
#
# Feather - https://www.adafruit.com/product/2821
# FeatherWing - https://www.adafruit.com/product/2928
#
# The pca9685.py and servo.py files from this repository must be copied to the
# esp8266
#  https://github.com/DocVaughan/micropython-adafruit-pca9685
#
#
#
# Created: 01/30/19
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

from machine import Pin, I2C
import time

# Imports for the servo FeatherWing
import pca9685
import servo

# Construct an I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

# Define the servos instance
# In the case of the feather it will contain 8 possible servos
servos = servo.Servos(i2c)

# We'll just be controlling servo number 0 here
SERVO_NUMBER = 0
DESIRED_ANGLE = 84

try:
    while(True):
        # Move the servo in position DESIRED_ANGLE degrees and hold there indefinitely
        servos.position(SERVO_NUMBER, DESIRED_ANGLE)
finally:
    # Now, release the servo
    servos.release(SERVO_NUMBER)
