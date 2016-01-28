
/* ----------------------------------------------------------------------------

esp8266_LEDblink.ino

Blinking the LED of an Adafruit Huzzah esp8266

From: 
  https://learn.adafruit.com/adafruit-huzzah-esp8266-breakout/using-arduino-ide

Created: 01/27/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <stdio.h>

void setup() {
  pinMode(0, OUTPUT);
}


void loop() {
  digitalWrite(0, HIGH);
  delay(500);
  digitalWrite(0, LOW);
  delay(500);
}
