#! /usr/bin/env python

###############################################################################
# esp32_MicroPy_boot_boilerplate.py
#
# base boot.py boilerplate code for MicroPython running on the esp8266
# Copy relevant parts and/or file with desired settings into boot.py on the esp32 
#
# The boot.py will be run once at every startup or reset. Configuration, etc 
# should happen in this file.
#
#
# Created: 07/23/17
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
# TODO:
#   * As of 07/23/17, the WEBREPL is not available for esp32 MicroPython port
###############################################################################

# import webrepl # As of 07/23/17, the WEBREPL is not available for esp32
import time
import machine

# Create a pin object for the onboard LED
# On the Wemos esp32 the onboard LED is pin 5
# On the Adafruit Feather it is pin 13
# On the ESP32 Dev board it is pin 16
LED = machine.Pin(5, machine.Pin.OUT)
LED.value(1) # Turn the pin off to start

WIFI_SSID = "SSID"
WIFI_PASSWORD = "password"

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
            LED.value(not LED.value()) # Toggle the LED while trying to connect
            
            # compute time difference since we started looking for the network
            # If it's greater than 10s, we'll time out and just start up as 
            # an access point.
            delta = time.ticks_diff(time.ticks_ms(), start) 
            if delta > 10000:
                print('\r\nTimeout on network connection. Please:')
                print(' * check the SSID and password \r\n * connect to the esp32 Access Point\r\n')
                break
            
    print('Network Configuration:', sta_if.ifconfig())
    LED.value(1) # Turn off the LED connected


if CONNECT_AS_STATION:
    do_connect()

# Also set up an access point
ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)                  # activate the interface
ap.config(essid='ESP32-AP')      # set the ESSID of the access point

# Start the webREPL
# Connect via http://micropython.org/webrepl/
# or using the .html file from https://github.com/micropython/webrepl
# As of 07/23/17, the WEBREPL is not available for esp32
# webrepl.start()

