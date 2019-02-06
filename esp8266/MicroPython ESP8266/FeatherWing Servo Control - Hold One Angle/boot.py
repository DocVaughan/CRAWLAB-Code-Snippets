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
from machine import Pin

# Create a pin object for the esp8266 onboard LED
pin = Pin(2, Pin.OUT)
pin.value(1) # Turn the LED off to start

WIFI_SSID = "SSID"
WIFI_PASSWORD = "PASSWORD"

# Set to true to connect to the WIFI network identified by the parameters above
# We'll leave the access point open too, for easy debugging/programming
CONNECT_AS_STATION = True

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    
    wifi_attempts = 0
    
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected() and wifi_attempts < 20:
            print('.')
            time.sleep_ms(250)
            pin.value(not pin.value()) # Toggle the LED while trying to connect

            # Increment the counter on the number of attemps
            wifi_attempts = wifi_attempts + 1
    
    if sta_if.isconnected():
        print('Network Configuration:', sta_if.ifconfig())
        pin.value(1) # Turn off the LED connected
    else:
        print('Did not connect to Wifi')


# Start the webREPL
# Connect via http://micropython.org/webrepl/
# or using the .html file from https://github.com/micropython/webrepl
webrepl.start()

if CONNECT_AS_STATION:
    do_connect()

