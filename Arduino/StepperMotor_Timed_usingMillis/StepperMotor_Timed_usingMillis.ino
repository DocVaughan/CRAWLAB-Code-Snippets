
// -----------------------------------------------------------------------------
// StepperMotor_Timed_usingMillis
//
// Runs a stepper motor a equal number of steps in two directions
// Timing is based on the millis() function
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
//    - shorten delay time between checking open/close state
// -----------------------------------------------------------------------------

#include <AFMotor.h>

// Define a stepper motor object
//   syntax: AF_Stepper motor(steps/revolution, motor_port);
AF_Stepper motor(200, 2);

// Define motor control constants
byte method = SINGLE;   // Options are SINGLE, DOUBLE, INTERLEAVE, MICROSTEP
double num_steps = 200; // Define the number steps to move the motor

    
// Define the times to use - all are in ms and variable type unsigned long
// This means that the maximum time is:
//   4,294,967,295 ms      or
//      42,949,672 seconds or
//          71,582 minutes or
//           1,193 hours   or
//              49 days
//
// Define the time to keep the door open in ms (1000ms = 1s)
unsigned long time_open = 5000; 

// Define the time to keep the door closed in ms (1000ms = 1s)
unsigned long time_closed = 5000; 

// Define the variables to store when the door was opened or closed
unsigned long opened_time;
unsigned long closed_time;


// This code runs only at startup
void setup() {
  Serial.begin(9600);          // set up Serial library at 9600 bps
  motor.setSpeed(20);          // 20 rpm  
 
  // Print the method to the debug window:
  // 1 = SINGLE
  // 2 = DOUBLE
  // 3 = INTERLEAVE
  // 4 = MICROSTEP
  Serial.print("Stepping method: ");
  Serial.println(method); 
  
  // Open the door when the code first runs
  Serial.println();
  Serial.println("Opening the door...");
  
  // syntax: step(number of steps, direction, method)
  // Note: step command is blocking, nothing else will run until it finishes
  motor.step(num_steps, FORWARD, method); 
  
  // save the time when the door was first opened
  opened_time = millis();
  
}


// the loop() function loops forever
void loop() {  
  
  while(1) // This while loop waits for the time to close
  {
    if( millis() - opened_time > time_open)
    {
      Serial.println("Closing the door...");
      // syntax: step(number of steps, direction, method)
      // Note: step command is blocking, nothing else will run until it finishes
      motor.step(num_steps, BACKWARD, method); 
      
      // save the time when the door was closed
      closed_time = millis();
     ;
      
      // break the while loop
      break;
    }
    
    // Some other code here
    
    // Pause 10ms before checking the time again
    delay(10)
  }
  
  while(1) // This while loop waits for the time to open
  {
    if( millis() - closed_time > time_closed)
    {
      Serial.println();
      Serial.println("Opening the door...");
      // syntax: step(number of steps, direction, method)
      // Note: step command is blocking, nothing else will run until it finishes
      motor.step(num_steps, FORWARD, method); 
      
      // save the time when the door was closed
      opened_time = millis();
      
      // break the while loop
      break;
    }
        
    // Some other code here
    
    // Pause 10ms before checking the time again
    delay(10)
  }
}
