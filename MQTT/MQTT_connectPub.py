#! /usr/bin/env python

##########################################################################################
# MQTT_connectPUB.py
#
# Basic MQTT topic publication via persistant client connection
# This is *WAY* faster than repeated single publications
#
#
# Created: 01/19/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 01/28/16 - JEV - joshua.vaughan@louisiana.edu
#       - added __future__ imports
#       - improved time formatting in send
#
##########################################################################################

from __future__ import print_function

import paho.mqtt.client as mqtt
import datetime
import time

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

if USERNAME is not None:
    client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect


client.connect(HOST, PORT, 60)


counter = 0
while True:
    counter += 1
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     send_time = str(timestamp) + ' Count: ' + str(counter)
    send_time = str(counter % 49)
    client.publish("CRAWLAB/from_python", send_time, qos=0)
    print(send_time)
        
    time.sleep(0.1)
