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
#   *
#
##########################################################################################

import paho.mqtt.publish as publish
import time

counter = 0
while True:
    counter += 1
    send_time = str(time.time()) + ' Count: ' + str(counter)
    publish.single("CRAWLAB", send_time, hostname="iot.eclipse.org")
    time.sleep(1)
