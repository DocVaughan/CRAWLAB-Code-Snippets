
// -----------------------------------------------------------------------------
// StepperMotor_Timed_usingDelay
//
// Runs a stepper motor a equal number of steps in two directions
// Timing is based on the simple delay() function
// 
// Adapted from:
//   Adafruit Motor shield library
//   copyright Adafruit Industries LLC, 2009
//   this code is public domain, enjoy!
//
// For more info on AF_Stepper,
//   see https://learn.adafruit.com/afmotor-library-reference/af-stepper-class 
//
// For help identifying the stepper motor wiring,
//   see http://www.jasonbabcock.com/computing/breadboard/unipolar/index.html
//
// Created: 05/20/14 - Joshua Vaughan - joshua.vaughan@louisiana.edu
//
// Modified:
//  * 6/17/14 - Joshua Vaughan - joshua.vaughan@louisiana.edu
//    - better commenting
//    - added link to stepper motor wiring guide
// -----------------------------------------------------------------------------

#include <AFMotor.h>

// Define a stepper motor object
//   syntax: AF_Stepper motor(steps/revolution, motor_port);
AF_Stepper motor(200, 2);

// Define program constants
byte method = SINGLE;   // Options are SINGLE, DOUBLE, INTERLEAVE, MICROSTEP
double num_steps = 200; // Define the number steps to move the motor


void setup() {
  Serial.begin(9600);          // set up Serial library at 9600 bps

  motor.setSpeed(20);          // 20 rpm  
 
  Serial.print("Stepping method: ");
  Serial.println(method); 
}

void loop() {  
  // syntax: step(number of steps, direction, method)
  // Note: step command is blocking, nothing else will run until it finishes
  motor.step(num_steps, FORWARD, method); 
  
  // Pause 1000ms
  delay(1000);
  
  // syntax: step(number of steps, direction, method)
  // Note: step command is blocking, nothing else will run until it finishes
  motor.step(num_steps, BACKWARD, method); 

  // Pause 1000ms  
  delay(1000);
}
