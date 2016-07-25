#! /usr/bin/env python

###############################################################################
# esp8266_MicroPy_main_MQTT_SerialBridge.py
#
# MQTT code for MicroPython running on the esp8266
# Copy relevant parts and/or file with desired settings into main.py on the esp8266 
#
# This code will listen on the CRAWLAB/esp8266/to topic. It will pass all
# messages received on that topic through to the serial output. It will also 
# pass all messages received over serial to the CRAWLAB/esp8266/from MQTT topic
#
# This makes this script a good candiate for use with microcontrollers without
# WiFi. Set up the serial communication between the esp8266 and the 
# microcontroller, then send messages to/from the correct topics.
#
# Note: You should probably change the topic names to be more relevant to the
# robot/system on which you are using this code.
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

CLIENT_ID = ubinascii.hexlify(machine.unique_id()) # MQTT require a unique ID
SUB_TOPIC = b'CRAWLAB/esp8266/to'         # Subscribe to this topic
PUB_TOPIC = b'CRAWLAB/esp8266/from'       # Publish to this topic

# Define a button - Many ESP8266 boards have active-low "flash" button on GPIO0
button = machine.Pin(0, machine.Pin.IN)

# set up the UART (serial) port
uart = machine.UART(0, 115200, timeout=0)

# String that will hold the message to send over MQTT
mqtt_message = ''

def subscriction_callback(topic, msg):
    # If data is received over MQTT, echo the full message over UART
    # When using on a robot or system, you probably want to remove the
    # 'From MQTT: ' part of the message.
    uart.write('From MQTT: {:s}\r\n'.format(msg))


# Blink the LED every 100ms to indicate we made it into the main.py file
for _ in range(10):
    time.sleep_ms(100)
    led.value(not led.value()) # Toggle the LED


# Make sure the LED is off
led.high()

# Create a MQTTClient instance.
mqtt = MQTTClient(CLIENT_ID, HOST, port=PORT)

# Subscribed messages will be delivered to this callback
mqtt.set_callback(subscriction_callback)

# Connect to the MQTT server
mqtt.connect()

# Define the topic to subscribe to
mqtt.subscribe(SUB_TOPIC)
print('\nMQTT:\n  Connected to: {}:{}\n  Subscribed to: {:s}\n  Publishing to: {:s}'.format(HOST, PORT, SUB_TOPIC, PUB_TOPIC))

try:
    while True:
        # This is the non-blocking method to check if there are MQTT messages
        mqtt.check_msg()
        
        # This attempts to read the UART until a newline character
        # Because we specified a timeout=0, when initializing the UART. It will
        # not block and instead returns the characters that it can read, even
        # if a newline isn't present. This means that we need to check for a newline
        # and be smart about processing the bytes/characters that were able 
        # to receive if one was not present.
        uart_message = uart.readline()

        if uart_message:
            # Toggle the LED for every piece of serial data received
            # This is useful for debugging, but you might want to disable
            # if the data rate is high
            led.value(not led.value()) 

            # Now, check the message that was received. 
            if uart_message.endswith('\n'): # If we received a full line,
                # then publish it directly
                mqtt.publish(PUB_TOPIC, uart_message)
                
                # and empty the mqtt_message
                # Note: This means we are losing data from some prior serial
                # commands that didn't complete with a newline. For some/many
                # applications this is probably okay. If not, you need to be
                # more careful here.
                mqtt_message = ''

            elif uart_message != b'\n': 
                # else if the byte was not a newline character, append it to the 
                # mqtt_message. In this case, we are receiving a byte stream
                # and attempting to recreate the full string being sent. 
                # Micropython is basically Python3, so we need to indicate
                # the type of encoding for the message/string, decode it,
                # then append it to the existing message.
                mqtt_message = mqtt_message + uart_message.decode('utf-8')

            else:#  else the current byte we read was a newline
                # The newline indicates the end of a properly terminated message,
                # so we can send the message now.

                # Publish the message constructed from the byte sequence
                # MicroPython is basically Python3, so we need to indicate
                # the type of encoding for the message/string. 
                mqtt.publish(PUB_TOPIC, mqtt_message.encode('utf-8'))
                
                # Then, empty the message
                mqtt_message = ''
finally:
    mqtt.disconnect()

