#! /usr/bin/env python

##########################################################################################
# BBB_DualServo_Workaround.py
#
# Working around bugs in the Adafruit library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/03/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

# import numpy as np

import Adafruit_BBIO.PWM as PWM

# class Servo():
# 
#     def __init__(self, servo_pin):
#         # Define duty cycle parameters for all servos
#         self.duty_min = 3.
#         self.duty_max = 14.5
#         self.duty_span = self.duty_max - self.duty_min
#         self.duty_mid = ((90.0 / 180) * self.duty_span + self.duty_min)
#         
#         self.servo_pin = servo_pin
#         PWM.start(self.servo_pin, 0)#self.duty_mid)
# 
#     def set_servo_angle(self, angle):
#         angle_f = float(angle)
#         duty = ((angle_f / 180) * self.duty_span + self.duty_min)
#         PWM.set_duty_cycle(self.servo_pin, duty)
# 
#     def close_servo(self):
#         PWM.stop(self.servo_pin)
#         PWM.cleanup()


if __name__ == "__main__":
    duty_min = 3.
    duty_max = 14.5
    duty_span = duty_max - duty_min
    duty_mid = ((90.0 / 180) * duty_span + duty_min)
    
    PWM.start("P9_29", duty_mid)
    PWM.start("P9_31", duty_mid)
    PWM.set_frequency("P9_29", 60.0)
    PWM.set_frequency("P9_31", 60.0)

    while True:
        angle = raw_input("Angle (0 to 180 x to exit):")
        if angle == 'x':
            PWM.stop("P9_29")
            PWM.stop("P9_31")
            PWM.cleanup()
            break

        angle_f = float(angle)
        duty = ((angle_f / 180) * duty_span + duty_min)
        
        PWM.set_duty_cycle("P9_29", duty)
        PWM.set_duty_cycle("P9_31", duty)
