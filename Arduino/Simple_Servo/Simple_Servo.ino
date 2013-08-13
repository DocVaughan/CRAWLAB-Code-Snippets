#include <Servo.h> 

Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
 
void setup() 
{ 
  myservo.attach(8);  // attaches the servo on pin 8 to the servo object 

  //initialize the serial connection
  Serial.begin(9600);
} 
 
 
void loop() 
{ 
    // if there's any serial data available, read it:
    while (Serial.available() > 0) {

    // look for the next valid integer in the incoming serial stream:
    pos = Serial.parseInt(); 
    
    Serial.print("Moving to angle ");
    Serial.println (pos);
    
    myservo.write(pos);5
    }
} 
