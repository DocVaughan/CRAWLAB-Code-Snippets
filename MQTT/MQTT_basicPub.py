#! /usr/bin/env python

##########################################################################################
# MQTT_basicPub.py
#
# Basic MQTT topic publication
#
# Adapted from: pub-single.py 
#   http://git.eclipse.org/c/paho/org.eclipse.paho.mqtt.python.git/tree/examples
#
# Created: 01/14/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 03/29/16 - JEV - joshua.vaughan@louisiana.edu
#       - from __future__ imports for Python 2 users
#
##########################################################################################

from __future__ import print_function

import paho.mqtt.publish as publish
import datetime
import time

## Eclipse
HOST = 'iot.eclipse.org'
PORT = 1883
AUTH = None

counter = 0
while True:
    counter += 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_time = str(timestamp) + ' Count: ' + str(counter)
    publish.single("CRAWLAB/from_python", send_time, hostname = HOST, port = PORT, auth = AUTH)
    time.sleep(0.2)
