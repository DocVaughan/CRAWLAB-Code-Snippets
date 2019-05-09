## LoRa_HeartBeat_receiver

Arduino sketch to receive heartbeat messages and toggle the onboard LED and print output to the serial monitor based on current status. The heartbeat sent has the format `$ULheartbeat`, which is checked by the receiver. It must be properly received *and* parsed to count as a received packet. If `MAX_MISSED_HEARTBEATS` or more heartbeats are missed consecutively, then the LED is lit solid red.

Intended for use with the [Adafruit Feather M0 with LoRa Radio](https://www.adafruit.com/product/3178)

Modified from the example code at [Adafruit's Tutorial](https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module/using-the-rfm-9x-radio)
