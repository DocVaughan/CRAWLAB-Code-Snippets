This folder contains CircuitPython code for the sender and receiver for a heartbeat-based E-stop using a digital output from the board to control a relay to cut the power to the drive components.

If `MAX_MISSED_HEARTBEATS` or more heartbeats are missed consecutively, then the relay output is turned off and the normally open relay opens.

Any data received is considered a heartbeat, which is bad practice, in general. Please see [](), for properly parsing a coded heartbeat signal.

*Note:* The files do not have headers, as the flash on the chips will be nearly full after installing CircuitPython and loading the necessary libraries.