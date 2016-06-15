/* ----------------------------------------------------------------------------

PID.c

PID controller, ideas borrowed heavily from:
  * http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
  * https://github.com/br3ttb/Arduino-PID-Library/
  
This implementation assumes that the controller is being called in an interrupt
 meaning it's running in "soft real time", or there's approx. constant time between
 calls. It also assumes that the sampleTime does not change during operation.

Created: 06/15/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include "PID.h"

PID set_up_PID(double Kp, double Ki, double Kd, 
               double outMax, double OutMin, double sampleTime) {
    /* Convenience function to fill a PID struct with the necessary parameters 
       to implement a PID controller.
       
       Arguments: 
         Kp : Proportional gain
         Ki : Integral gain
         Kd : Derivative gain
         outMax : maximum output from the PID controller
         outMin : minium output from the PID controller
         sampleTime : the sampleTime the control loop is running at
         
       Returns:
         A struct containing all the variables initialized to use the PID 
         controller
    */
    
    PID pid = {Kp, Kd, Ki, 0.0, 0.0, outMax, outMin, 1, sampleTime};
    
    return pid;
}
    

double compute_PID(double measurement, double desired, PID *pid) {
    /* Function that computes the PID controller output 
    
       Arguments:
         measurement : current value of the variable we're trying to control
         desired : desired value of the variable we're trying to control
         *pid : pointer to the PID struct containing the controller info to use
         
       Returns:
         double presenting the output of the PID algorithm
    */
    
    // Check if the controller is on, if not, return 0 output from it
    if (!pid->ControlON) {
        return 0.0
    }
    else {
        double kp = pid->Kp
        double ki = pid->Ki * pid->sampleTime;
        double kd = pid->Kd

        // define the current error and its derivative
        double error = desired - measurement;
        double error_deriv = (measurement - pid->lastMeasurement) / pid->sampleTime;
        
        // calculate, then limit the integral term to within the limits
        pid->integralTerm += ki * error;
        
        if (pid->integralTerm > pid->outMax) {
            pid->integralTerm = pid->outMax;
        else if (pid->integralTerm < pid->outMin ) {
            pid->integralTerm = pid->outMin;
        }
        
        double output = kp * error + pid->integralTerm + kd * error_deriv;
    
        pid->lastMeasurement = measurement;
        
        return output;
    }
}
    

void change_PID_limits(double min, double max, PID *pid) {
    /* Function to adjust the limits of the PID controller in a way that 
       results in continued smooth operation. More elegant than changing the 
       struct directly, because we update the integralTerm too.
       
       Arguments:
         min : new minumum output value
         max : new maximum output value
         *pid : pointer to struct containing the PID controller to modify
    */
    
    // Change the values in the struct
    pid->outMin = min;
    pid->outMax = max;
    
    // Also update the running integralTerm
    if (pid->integralTerm > pid->outMax) {
        pid->integralTerm = pid->outMax;
    else if (pid->integralTerm < pid->outMin) {
        pid->integralTerm = pid->outMin;
    }
}
        
    
    
    
    
                  