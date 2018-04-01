#! /usr/bin/env python

##########################################################################################
# MQTT_connectPUB_json.py
#
# Basic MQTT topic publication of json formatted data via persistant client
# connection. This is *WAY* faster than repeated single publications
#
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
#
##########################################################################################

from __future__ import print_function

import paho.mqtt.client as mqtt
import datetime
import time
import json


# Define the MQTT broker settings
## Eclipse
HOST = 'iot.eclipse.org'
PORT = 1883
USERNAME = None
PASSWORD = None

## MQTT Dashboard
# HOST = 'broker.mqttdashboard.com'
# PORT = 1883
# USERNAME = None
# PASSWORD = None


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))


client = mqtt.Client()

# check for a defined username. If we have defined one, set the username and 
# password for the server,
if USERNAME is not None:
    client.username_pw_set(USERNAME, PASSWORD)

# Set up the callback for the connection. The function on_connect() gets called
# on a successful connetion
client.on_connect = on_connect

# Attempt to connect to the MQTT broker
client.connect(HOST, PORT, 60)

# Initialize the counter
counter = 0

# Initialize the _last_time variable. Will be used to send on more-regular 
# intervals that a sleep timer. This is a bit of a hack, but one that works 
# relatively well for simple things like this.
last_time = time.time()

deltaT = 0.2 # The period to send (s)

while True:
    
    current_time = time.time()
    
    if current_time - last_time >= deltaT:
        counter += 1
    
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
        message = {'counter': counter, 'time': timestamp}
        message_string = json.dumps(message)
    
        client.publish("CRAWLAB/from_python", message_string, qos=0)
        
        last_time = current_time
