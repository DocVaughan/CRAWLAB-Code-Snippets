## LoRa Heartbeat Receiver with NeoPixel Status
Arduino sketch to receive heartbeat messages and change the color of the a NeoPixel strip based on current status. The heartbeat sent has the format `$ULheartbeat`, which is checked by the receiver. It must be properly received *and* parsed to count as a received packet. If `MAX_MISSED_HEARTBEATS` or more heartbeats are missed consecutively, then the onboard LED is lit solid red and the strip is changed to red. If heartbeats are being received, it will be green. The strip also displays a "Knight Rider" effect, since motion is easier seen than static objects.

Intended for use with the [Adafruit Feather M0 with LoRa Radio](https://www.adafruit.com/product/3178)

Modified from the example code at [Adafruit's Tutorial](https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module/using-the-rfm-9x-radio)
