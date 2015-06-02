#! /usr/bin/env python

##########################################################################################
# BBB_BasicInterrrupts.py
#
# Basic use of interrupts on the Beagle Bone Black
#
# Requires - Adafruit BeagleBone IO Python library
#
# Adapted from Raspberry Pi Version at: 
#   http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-2
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/28/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import Adafruit_BBIO.GPIO as GPIO

# GPIO P8_14 and P8_16 as an inputs
GPIO.setup('P8_14', GPIO.IN)
GPIO.setup('P8_16', GPIO.IN)
  
# # now we'll define the threaded callback function  
# # this will run in another thread when our event is detected  
def my_callback(channel):  
    print 'Rising edge detected on P8_16 Button even though, in the main thread,'  
    print 'we are still waiting for a falling edge - how cool?\n'  



# The GPIO.add_event_detect() line below set things up so that  
# when a rising edge is detected, regardless of whatever   
# else is happening in the program, the function 'my_callback' will be run  
# It will happen even while the program is waiting for  
# a falling edge on the other button.  
GPIO.add_event_detect('P8_16', GPIO.RISING, callback=my_callback, bouncetime=200)  

try:  
    print 'Waiting for falling edge on P8_14 - right button'  
    GPIO.wait_for_edge('P8_14', GPIO.RISING)  
    print 'Falling edge detected. Here endeth the second lesson.'  
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    
    
GPIO.cleanup()           # clean up GPIO on normal exit  