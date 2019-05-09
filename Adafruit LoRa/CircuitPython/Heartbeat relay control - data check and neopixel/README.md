## A Heartbeat-based Relay E-stop with NeoPixel Status
This folder contains CircuitPython code for the sender and receiver for a heartbeat-based E-stop using a digital output from the board to control a relay to cut the power to the drive components.

The heartbeat sent has the format `$ULheartbeat`, which is checked by the receiver. It must be properly received *and* parsed to count as a received packet. If `MAX_MISSED_HEARTBEATS` or more heartbeats are missed consecutively, then the relay output is turned off and the normally open relay opens.

A NeoPixel strip is controlled to indicate the state of the system.

*Note:* 
* The files do not have headers, as the flash on the chips will be nearly full after installing CircuitPython and loading the necessary libraries.
* As of 05/09/19, there appear to be issues with the NeoPixel controller.