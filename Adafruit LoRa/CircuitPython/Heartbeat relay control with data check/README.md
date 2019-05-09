## Heartbeat with Data Check
This folder contains CircuitPython code for the sender and receiver for a heartbeat-based E-stop using a digital output from the board to control a relay to cut the power to the drive components.

The heartbeat sent has the format `$ULheartbeat`, which is checked by the receiver. It must be properly received *and* parsed to count as a received packet. If `MAX_MISSED_HEARTBEATS` or more heartbeats are missed consecutively, then the relay output is turned off and the normally open relay opens.

Any data received is considered a heartbeat, which is bad practice, in general. Please see [](), for properly parsing a coded heartbeat signal.
