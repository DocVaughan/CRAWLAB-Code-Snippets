#! /usr/bin/env python

##########################################################################################
# BBB_PyBBIO_servos.py
#
# Using PyBBIO (not Adafruit) to control servos
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
##########################################################################################

import bbio
import bbio.libraries.Servo as Servo

servo1 = Servo(PWM0B)

if __name__ == '__main__':
    bbio.bbio_init()
    
    while True:
        angle = raw_input("Angle (0 to 180 x to exit):")
        if angle == 'x':
            bbio.bbio_cleanup()
            break

        servo1.write(angle)