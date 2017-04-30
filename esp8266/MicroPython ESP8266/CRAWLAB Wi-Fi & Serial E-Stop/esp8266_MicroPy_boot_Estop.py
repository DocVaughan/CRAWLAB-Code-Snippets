#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_boot_boilerplate.py
#
# base boot.py boilerplate code for MicroPython running on the esp8266
# Copy relevant parts and/or file with desired settings into boot.py on the esp8266 
#
# The boot.py will be run once at every startup or reset. Configuration, etc 
# should happen in this file.
#
#
# Created: 06/04/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import webrepl
import time
import machine

# Create a pin object for the esp8266 onboard LED
pin = machine.Pin(2, machine.Pin.OUT)
pin.high() # Turn the pin off to start

WIFI_SSID = "SSID"
WIFI_PASSWORD = "PASS"

# Set to true to connect to the WIFI network identified by the parameters above
# We'll leave the access point open too, for easy debugging/programming
CONNECT_AS_STATION = True

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    
    start = time.ticks_ms() # get millisecond counter
    
    
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            print('Waiting for connection...')
            time.sleep_ms(500)
            pin.value(not pin.value()) # Toggle the LED while trying to connect
            
            # compute time difference since we started looking for the network
            # If it's greater than 10s, we'll time out and just start up as 
            # an access point.
            delta = time.ticks_diff(time.ticks_ms(), start) 
            if delta > 10000:
                print('\r\nTimeout on network connection. Please:')
                print(' * check the SSID and password \r\n * connect to the esp8266 Access Point\r\n')
                break
            
    print('Network Configuration:', sta_if.ifconfig())
    pin.high() # Turn off the LED connected


if CONNECT_AS_STATION:
    do_connect()


# Start the webREPL
# Connect via http://micropython.org/webrepl/
# or using the .html file from https://github.com/micropython/webrepl
webrepl.start()

