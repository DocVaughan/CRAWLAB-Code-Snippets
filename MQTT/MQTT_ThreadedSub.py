#! /usr/bin/env python

##########################################################################################
# MQTT_ThreadedSub.py
#
# Basic implementation of a threaded MQTT client
#
# From: http://eclipse.org/paho/clients/python/
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/14/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 01/28/16 - JEV - joshua.vaughan@louisiana.edu
#       - added __future__ imports
#       - improved time formatting in status printing
#
#   * 03/29/16 - JEV - joshua.vaughan@louisiana.edu
#       - Python 3 bytes to string conversion
#
##########################################################################################

from __future__ import print_function

import paho.mqtt.client as mqtt
import datetime
import time

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


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CRAWLAB/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic + ' Received at: ' + str(time.time()) + ' Sent at: ' + str(msg.payload) + ' Latency: {:0.4f}'.format(time.time() - float(msg.payload)))
    print('Received Topic: ' + msg.topic + '\t Data: ' + msg.payload.decode(encoding='UTF-8'))

# Create the MQTT client instance
client = mqtt.Client()

# If a USERNAME has been defined use it and the password for log in
if USERNAME is not None:
    client.username_pw_set(USERNAME, PASSWORD)

# Set up the callback function for connection and message receiving
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT server defined by HOST and PORT with 60s timeout
client.connect(HOST, PORT, 60)

# Non-blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_start()

# This loop will run printing current time while also reading MQTT data
try: 
    while True:
        print('\n')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)
        
except (KeyboardInterrupt, SystemExit):
    client.loop_stop()