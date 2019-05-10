## LoRa_HeartBeat_sender_withStatus

Arduino sketch to send a heartbeat messages with the format `$ULheartbeat`, which is checked by the receiver. It looks for an acknowledgement from the receiver and outputs the status to the serial monitor.

Intended for use with the [Adafruit Feather M0 with LoRa Radio](https://www.adafruit.com/product/3178)

Modified from the example code at [Adafruit's Tutorial](https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module/using-the-rfm-9x-radio)
