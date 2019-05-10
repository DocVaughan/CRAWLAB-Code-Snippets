## LoRa_HeartBeat_sned_withOLEDStatus

Arduino sketch to send a heartbeat messages with the format `$ULheartbeat`, which is checked by the receiver. It looks for an acknowledgement from the receiver and outputs the status to the serial monitor and an OLED screen. 

Intended for use with the [Adafruit Feather M0 with LoRa Radio](https://www.adafruit.com/product/3178) and [Adafruit FeatherWing OLED](https://www.adafruit.com/product/2900).

Modified from the example code in Adafruit's [LoRA](https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module/using-the-rfm-9x-radio) and [OLED](https://learn.adafruit.com/adafruit-oled-featherwing) tutorials.
