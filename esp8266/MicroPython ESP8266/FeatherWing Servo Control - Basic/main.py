###############################################################################
# main.py
#
# main script for basic servo control using an Adafruit esp8266 feather with 
# their 8-channel PWM/servo FeatherWing
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

# Move the servo in position 80deg
# 80 deg was actually center on the servo I was testing on
# The default possible range is 0-180. However, note that most servos, even
# if advertised as having that range, do not. +/-60 deg around the center
# is much more reliable. +/-45deg around center is even better.
servos.position(SERVO_NUMBER, 80)
time.sleep(1)

# Now, move to 50deg 
servos.position(SERVO_NUMBER, 50)
time.sleep(1)

# Move from 50 deg to 110deg with a 100ms sleep between each angle command
for angle in range(60):
    servos.position(SERVO_NUMBER, 50+angle)
    time.sleep_ms(100)
    
# Move back to 80 degrees
# 80 deg was actually center on the servo I was testing on
servos.position(SERVO_NUMBER, 80)
time.sleep(1)

# Now, release the servo
servos.release(0)
