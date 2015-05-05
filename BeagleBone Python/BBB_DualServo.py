#! /usr/bin/env python

##########################################################################################
# BBB_DualServo.py
#
# Script to run two servos in coordination
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

import Adafruit_BBIO.PWM as PWM
import time

class Servo():

    def __init__(self, servo_pin):
        # Define duty cycle parameters for all servos
        self.duty_min = 3.
        self.duty_max = 14.5
        self.duty_span = self.duty_max - self.duty_min
        self.duty_mid = ((90.0 / 180) * self.duty_span + self.duty_min)
        
        self.servo_pin = servo_pin
        PWM.start(self.servo_pin, self.duty_mid, 60.0)

    def set_servo_angle(self, angle):
        angle_f = float(angle)
        duty = ((angle_f / 180) * self.duty_span + self.duty_min)
        PWM.set_duty_cycle(self.servo_pin, duty)

    def close_servo(self):
        PWM.stop(self.servo_pin)


if __name__ == "__main__":

    time.sleep(1)
    
#     # Workaround for Adafruit library bug
#     PWM.start('P9_29', 0)
#     PWM.start('P9_31', 0)
#     PWM.set_frequency('P9_29', 60.0)
#     PWM.set_frequency('P9_31', 60.0)

    servo_left = Servo('P9_29')
    servo_right = Servo('P9_31')
    
#     servo_left.set_servo_angle(90)
#     servo_right.set_servo_angle(90)

    try:
        while True:
            angle = raw_input("Angle (0 to 180 x to exit):")
            
            if angle == 'x':
                servo_left.close_servo()
                servo_right.close_servo()
                break

            servo_left.set_servo_angle(angle)
            servo_right.set_servo_angle(angle)
    
    except KeyboardInterrupt:
        servo_left.close_servo()
        servo_right.close_servo()
        PWM.cleanup()
    