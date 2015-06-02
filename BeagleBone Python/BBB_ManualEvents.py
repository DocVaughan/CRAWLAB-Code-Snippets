#! /usr/bin/env python

##########################################################################################
# BBB_BasicInterrrupts.py
#
# Manually generated event watch on the Beagle Bone Black to avoid bug in 
#  Adafruit BBIO library
#
# Requires - Adafruit BeagleBone IO Python library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/02/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################


import Adafruit_BBIO.GPIO as GPIO
import logging
import threading
import time


TOP_LIMIT = 'P8_14'     # Pin of top limit switch
BOTTOM_LIMIT = 'P8_16'  # Pin of bottom limit switch
pressed = False

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

# GPIO P8_14 and P8_16 as an inputs
GPIO.setup('P8_14', GPIO.IN)
GPIO.setup('P8_16', GPIO.IN)


def check_switch(switch_pin):  
    global pressed
    logging.debug('Thread starting to read pin {}.'.format(switch_pin))  
    
    while True:
        if GPIO.input(switch_pin):
            logging.debug('{} presssed'.format(switch_pin))
            with lock:
                pressed = True
            time.sleep(0.2)
        elif pressed:
            with lock:
                pressed = False
        time.sleep(0.01)

# The GPIO.add_event_detect() line below set things up so that  
# when a rising edge is detected, regardless of whatever   
# else is happening in the program, the function 'my_callback' will be run  
# It will happen even while the program is waiting for  
# a falling edge on the other button.  
# GPIO.add_event_detect('P8_16', GPIO.RISING, callback=my_callback, bouncetime=200)  
# GPIO.add_event_detect('P8_16', GPIO.RISING, bouncetime=200)  

switch_thread = threading.Thread(name = 'check_switch', target = check_switch, args = ('P8_16',))
switch_thread.daemon = True
switch_thread.start()

# Create a lock
lock = threading.Lock()

try:  
    logging.debug('Waiting for falling edge on P8_14.')  
    GPIO.wait_for_edge('P8_14', GPIO.RISING)  
    logging.debug('Falling edge on P8_14 detected.')
    time.sleep(1)
    
    logging.debug('/nNow, let\'s try it in a for loop')
    while not GPIO.input('P8_14'):
        logging.debug(pressed)
        time.sleep(1)

  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    
    
GPIO.cleanup()           # clean up GPIO on normal exit  