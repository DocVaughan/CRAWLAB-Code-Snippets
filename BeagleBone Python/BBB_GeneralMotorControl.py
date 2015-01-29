#! /usr/bin/env python

###############################################################################
# BBB_BasicMotorControl.py
#
# Basic test of motor control using the SparkFun TB6612FNG breakout board
# 
# Requires - Adafruit BeagleBone IO Python library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/09/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import math

class motor(object):
    """ Convenience class for controlling a motor
    
    Arguments
      ControlPin1 : the x01 pin 
      ControlPin2 : the x02 pin
      PWMpin : the PWM pin
      STBYpin : the STBY (standby) pin on the board
      
    Other atributes
      isRunning : Boolean describing if motor is running or not
      speed : current speed of the motor
      direction : current direction the motor is running 
                  =None if the motor is not currently moving
                  
    """
    def __init__(self, ControlPin1, ControlPin2, PWMpin, STBYpin):
        self.ControlPin1 = ControlPin1
        self.ControlPin2 = ControlPin2
        self.PWMpin = PWMpin
        self.STBYpin = STBYpin
        self.isRunning = False
        self.currentDirection = None
        self.currentSpeed = 0
        
        # Set up the GPIO pins as output
        GPIO.setup(self.STBYpin, GPIO.OUT)
        GPIO.setup(self.ControlPin1, GPIO.OUT)
        GPIO.setup(self.ControlPin2, GPIO.OUT)


    def start(self, speed, direction):
        """ method to start a motor 
    
        Arguments:
          speed : speed of the motor 0-100 (as percentage of max)
          direction : CW or CCW, for clockwise or counterclockwise
        """
        
        # Standby pin should go high to enable motion
        GPIO.output(self.STBYpin, GPIO.HIGH)
    
        # x01 and x02 have to be opposite to move, toggle to change direction
        if direction in ('cw','CW','clockwise'):
            GPIO.output(self.ControlPin1, GPIO.LOW)
            GPIO.output(self.ControlPin2, GPIO.HIGH)
        elif direction in ('ccw','CCW','counterclockwise'):
            GPIO.output(self.ControlPin1, GPIO.HIGH)
            GPIO.output(self.ControlPin2, GPIO.LOW)
        else:
            raise ValueError('Please enter CW or CCW for direction.')
    
        # Start the motor
        # PWM.start(channel, duty, freq=2000, polarity=0)
        if 0 <= speed <= 100:
            PWM.start(self.PWMpin, speed)
        else:
            raise ValueError("Please enter speed between 0 and 100, \
                              representing a percentage of the maximum \
                              motor speed.")

        # set the status attributes
        self.isRunning = True
        self.currentDirection = direction
        self.currentSpeed = speed

    def stop(self):
        """ redirects to a soft stop """
        self.soft_stop()


    def hard_stop(self):
        """ Method to hard stop an individual motor"""
        
        PWM.set_duty_cycle(self.PWMpin, 0.0)
        
        # set the status attributes
        self.isRunning = True
        self.currentDirection = None
        self.currentSpeed = 0


    def soft_stop(self):
        """ Method to soft stop (coast to stop) an individual motor"""
        
        # Make both control pins low
        GPIO.output(self.ControlPin1, GPIO.LOW)
        GPIO.output(self.ControlPin2, GPIO.LOW)
        PWM.stop(self.PWMpin)
        GPIO.output(self.STBYpin, GPIO.LOW)
        
        # set the status attributes
        self.isRunning = True
        self.currentDirection = None
        self.currentSpeed = 0.0


    def set_speed(self, newSpeed):
        """ Method to change the speed of the motor, direciton is unchanged
        
        Arugments
          newSpeed : the desired new speed 0-100 (as percentage of max)
        """
        
        PWM.set_duty_cycle(self.PWMpin, newSpeed)
        self.currentSpeed = newSpeed




if __name__ == '__main__':
    # Demonstrates the use of this class
    
    # Set up the pins - These are mutable, but *don't* change them
    STBY = 'P8_9'       # STBY pin on the breakout, must go low to enable motion
    A01 = 'P8_7'        # A01 pin on board, controls direction along with A02
    A02 = 'P8_8'        # A02 pin on board, controls direction along with A01
    PWMA = 'P8_13'      # PWMA pin on board, controls the speed of Motor A
    
    # Create the motorA instance of the class
    motorA = motor(A01, A02, PWMA, STBY)
    
    # We can check if it's running
    if motorA.isRunning:
        print 'Motor A is currently running.'
    else:
        print 'Motor A is not currently running.'


    # Now, let's run it for 2s, off for 2s, on for 2s... for 5 times
    # let's print that it's running each time too, using our inRunning attribute
    for index in range(2):
        motorA.start(100,'CCW')

         # We can check if it's running
        if motorA.isRunning:
            print 'Motor A is spinning {} at {}% of maximum speed.'.format(motorA.currentDirection, motorA.currentSpeed)

        time.sleep(2)
        print 'This is a hard stop. It effectively brakes.\n'
        motorA.hard_stop()
        time.sleep(2)
        
        motorA.start(100,'CW')

        # We can check if it's running
        if motorA.isRunning:
            print 'Motor A is spinning {} at {}% of maximum speed.'.format(motorA.currentDirection, motorA.currentSpeed)

        time.sleep(2)

        print 'This is a soft stop. It coasts to stop.\n'
        motorA.stop()
        time.sleep(2)


    # Let's vary the speed - we'll get fancy and use a sinusoidal variance
    motorA.start(75,'CW')
    lastTime = time.time()
    startTime = time.time()

    while time.time()-startTime < 30:
        speed = 75 + 25 * math.sin(0.25 * 2 * math.pi * (time.time()-startTime))
        motorA.set_speed(speed)
        
        if time.time() - lastTime > 1:
            print 'Motor A is spinning {} at {:>6.2f}% of maximum speed.'.format(motorA.currentDirection, motorA.currentSpeed)
            lastTime = time.time()
            
        time.sleep(0.01)
    
    motorA.stop()
    
    # We can still access pins and "raw" Adafruit library functions if needed
    GPIO.output(motorA.STBYpin, GPIO.LOW)