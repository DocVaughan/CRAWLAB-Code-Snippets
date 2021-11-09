#! /usr/bin/env python

###############################################################################
# odrive_basics.py
#
# Script demonstrating basic communications and control of the Odrive. 
#    * https://docs.odriverobotics.com
#    * https://docs.odriverobotics.com/api/odrive
#
# Some code modified from that at:
#    https://github.com/odriverobotics/ODrive/blob/master/tools/odrive_demo.py
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 11/08/21
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import time

import numpy as np
import matplotlib.pyplot as plt

import odrive               # Main odrive library/module
from odrive.enums import *  # Convenience constants

# Find a connected ODrive (this will block until you connect one)
print("Finding an Odrive...")
drive = odrive.find_any()

# Calibrate motor and wait for it to finish
print("Starting calibration...")
drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while drive.axis1.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

# Now, change to closed-loop control
drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# To read a value, simply read the property
print("Bus voltage is {:7.4f} VDC".format(drive.vbus_voltage))

# Or to change a value, just assign to the property
drive.axis1.controller.input_pos = 3.14
print("Position setpoint is {:.4f}".format(drive.axis1.controller.pos_setpoint))

# And this is how function calls are done:
for gpio_num in [1,2,3,4]:
    print('voltage on GPIO{:d} is {:.4f} Volt'.format(gpio_num, drive.get_adc_voltage(gpio_num)))

# A sine wave to test
start_time = time.monotonic()
# # try:
while True:
    setpoint = np.pi * np.sin(0.1 * 2 * np.pi * (time.monotonic() - start_time))
    print("Moving to {:7.4f}".format(setpoint))
    drive.axis1.controller.input_pos = setpoint
    time.sleep(0.01)
        
# except(KeyboardInterrupt):
    
    