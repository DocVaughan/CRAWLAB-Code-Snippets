#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_main_MQTT_to_Serial.py
#
# simple MQTT code for MicroPython running on the esp8266
# Copy relevant parts and/or file with desired settings into main.py on the esp8266 
#
# This code will listen on the CRAWLAB/esp8266/joystick topic. It will pass
# all messages received on that topic through to the serial output. This 
# makes this script a good candiate for use with microcontrollers without
# WiFi. Set up the serial communication between the esp8266 and the 
# microcontroller, then send messages to the correct topic.
#
# The main.py file will run immediately after boot.py
# As you might expect, the main part of your code should be here
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
TOPIC = b'CRAWLAB/esp8266/joystick'

def subscriction_callback(topic, msg):
    print(msg)
    # Toggle the onboard LED. You should probably disable this if
    # messages are being sent at a high rate
    led.value(not led.value())


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
mqtt.subscribe(TOPIC)
print('Connected to {}, subscribed to {} topic.'.format(HOST, TOPIC))

try:
    while 1:
        #micropython.mem_info()
        mqtt.wait_msg()
finally:
    mqtt.disconnect()

