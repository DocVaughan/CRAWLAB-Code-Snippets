#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_main_MQTT_basic.py
#
# simple MQTT code for MicroPython running on the esp8266
# Copy relevant parts and/or file with desired settings into main.py on the esp8266 
#
# This code will listen on the CRAWLAB/esp8266/LED topic
# If the message sent is:
#   - on, then the LED will be turned on
#   - off, then the LED will be turned off
#   - toggle, then the LED state will be toggled
#
# The main.py file will run immediately after boot.py
# As you might expect, the main part of your code should be here
#
# Created: 07/23/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

from umqtt.simple import MQTTClient
import ubinascii

# The modules below should have been imported in boot.py
# import webrepl
# import time
# import machine

# Constants for MQTT server 
# ## Eclipse
HOST = 'iot.eclipse.org'
PORT = 1883
USERNAME = None
PASSWORD = None

# MQTT Dashboard
# HOST = 'broker.mqttdashboard.com'
# PORT = 1883
# USERNAME = None
# PASSWORD = None

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
SUB_TOPIC = b'CRAWLAB/esp8266/LED'          # Subscribe to this topic
PUB_TOPIC = b'CRAWLAB/esp8266/button'       # Publish to this topic

# global variable to hold the current state of the LED
state = 0

# Define a button - Many ESP8266 boards have active-low "flash" button on GPIO0
button = machine.Pin(0, machine.Pin.IN)

def subscriction_callback(topic, msg):
    global state
    print((topic, msg))
    if msg == b'on':
        led.value(0)
        state = 1
    elif msg == b'off':
        led.value(1)
        state = 0
    elif msg == b'toggle':
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state


# Blink the LED every 100ms to indicate we made it into the main.py file
for _ in range(10):
    time.sleep_ms(100)
    led.value(not led.value()) # Toggle the LED
    time.sleep_ms(100)

# Make sure the LED is off
led.high()

# define a time, because we only want to send every 1s but received as fast as possible
# last_time = time.time()

mqtt = MQTTClient(CLIENT_ID, HOST, port=PORT)
# Subscribed messages will be delivered to this callback
mqtt.set_callback(subscriction_callback)
mqtt.connect()
mqtt.subscribe(SUB_TOPIC)
print('Connected to {}, subscribed to {} topic.'.format(HOST, SUB_TOPIC))

try:
    while True:
        while True:
            mqtt.check_msg()
            if button.value() == 0: # the button is active low
                break # if it's pressed break out of the internal while loop
            time.sleep_ms(20)
        print('Button Pressed')
        mqtt.publish(PUB_TOPIC, b'Button Pressed')
        time.sleep_ms(200)
finally:
    mqtt.disconnect()

