#! /usr/bin/env python

##########################################################################################
# MQTT_ThreadedSub.py
#
# Basic implementation of a threaded MQTT client, intended to receive json-formatted
# messages.
#
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 03/18/18
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
##########################################################################################

from __future__ import print_function

import paho.mqtt.client as mqtt
import datetime
import time
import json

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
    print('\nReceived Topic: ' + msg.topic)
    
    try:
        data = json.loads(msg.payload.decode(encoding='UTF-8'))
        print('Time = {}'.format(data['time']))
        print('Counter = {:d}'.format(data['counter']))

    except (AttributeError, TypeError):
        print('Data was not properly formatted json or had different keys than expected.')

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