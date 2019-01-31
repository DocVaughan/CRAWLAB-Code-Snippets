The main script here is for basic hobby-style-servo control using an [Adafruit esp8266 Feather](https://www.adafruit.com/product/2821) with their [8-channel PWM/servo FeatherWing](https://www.adafruit.com/product/2928). The angle command for the servo is issued over UDP.

The Wi-Fi SSID and password will have to be changes to meet your setup.

The `pca9685.py` and `servo.py` files from [this repository](https://github.com/DocVaughan/micropython-adafruit-pca9685) must be copied to the esp8266.