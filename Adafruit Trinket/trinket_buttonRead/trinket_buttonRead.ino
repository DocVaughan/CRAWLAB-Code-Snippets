      /*
  Button
  Turns on an LED when a switch connected from #0 to ground is pressed
 
  This example code is in the public domain.
 
  To upload to your Gemma or Trinket:
  1) Select the proper board from the Tools->Board Menu
  2) Select USBtinyISP from the Tools->Programmer
  3) Plug in the Gemma/Trinket, make sure you see the green LED lit
  4) For windows, install the USBtiny drivers
  5) Press the button on the Gemma/Trinket - verify you see
     the red LED pulse. This means it is ready to receive data
  6) Click the upload button above within 10 seconds
*/
 
#define SWITCH 0
#define LED 1
 
// the setup routine runs once when you press reset:
void setup() {
  Serial.begin(9600);
  
  // initialize the LED pin as an output.
  pinMode(LED, OUTPUT);
  // initialize the SWITCH pin as an input.
  pinMode(SWITCH, INPUT);
  // ...with a pullup
  digitalWrite(SWITCH, HIGH);
}
 
// the loop routine runs over and over again forever:
void loop() {
  Serial.println(digitalRead(SWITCH);
  
  if (! digitalRead(SWITCH)) {  // if the button is pressed
    digitalWrite(LED, HIGH);    // light up the LED
  } else {
    digitalWrite(LED, LOW);     // otherwise, turn it off
  }
}

