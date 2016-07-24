#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_boot_MQTT_to_Serial.py
#
# boot.py code for MicroPython running on the esp8266
# Copy relevant parts and/or file with desired settings into boot.py on the esp8266 
#
# The boot.py will be run once at every startup or reset. Configuration, etc 
# should happen in this file.
#
#
# Created: 07/24/16
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
led = machine.Pin(2, machine.Pin.OUT)
led.high() # Turn the pin off to start

WIFI_SSID = "your_WiFiSSID"
WIFI_PASSWORD = "your_password"

# Set to true to connect to the WIFI network identified by the parameters above
# We'll leave the access point open too, for easy debugging/programming
CONNECT_AS_STATION = True

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            print('.')
            time.sleep_ms(250)
            led.value(not led.value()) # Toggle the LED while trying to connect
            
    print('Network Configuration:', sta_if.ifconfig())
    led.high() # Turn off the LED connected


if CONNECT_AS_STATION:
    do_connect()


# Start the webREPL
# Connect via http://micropython.org/webrepl/
# or using the .html file from https://github.com/micropython/webrepl
webrepl.start()

