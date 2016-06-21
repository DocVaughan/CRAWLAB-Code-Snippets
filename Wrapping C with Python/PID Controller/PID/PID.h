/* ----------------------------------------------------------------------------

PID.h

Header file for PID controller

Created: 06/15/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

typedef struct {
    double Kp;                  // Proportional Gain
    double Kd;                  // Derivative Gain
    double Ki;                  // Derivative Gain
    double lastMeasurement;     // Measurement input remembered from last loop
    double integralTerm;        // Running total for integral term
    double outMax;              // Maximum value of output
    double outMin;              // Minimum value of output
    int controlON;              // 1 if controller is active, allows us to still keep track of controller even if not acting
    double sampleTime;          // the sample time being used in the interrupt
} PID;